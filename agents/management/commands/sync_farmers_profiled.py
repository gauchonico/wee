from django.core.management.base import BaseCommand
from agents.models import Agent
from cooperatives.models import Member
from django.contrib.auth.models import User
from django.db.models import F
from django.db.models import Q

class Command(BaseCommand):
    help = 'Syncs farmers_profiled counts with actual member assignments'

    def handle(self, *args, **options):
        # Get all agents
        agents = Agent.objects.all()
        
        # Get all members with their created_by information
        members = Member.objects.select_related('created_by').all()
        
        # Create a dictionary to store actual member counts
        actual_counts = {}
        unmatched_members = []
        
        # First, create a lookup dictionary for agents
        agent_lookup = {}
        for agent in agents:
            # Store by full name in first_name
            agent_lookup[agent.first_name.lower()] = agent
            # Store by full name in last_name
            agent_lookup[agent.last_name.lower()] = agent
            # Store by first part of name
            if ' ' in agent.first_name:
                first_part = agent.first_name.split()[0].lower()
                agent_lookup[first_part] = agent
            # Store by single name if it's a single name
            if not ' ' in agent.first_name:
                agent_lookup[agent.first_name.lower()] = agent
        
        for member in members:
            if member.created_by:
                # Try to find the agent by user's name
                user_name = f"{member.created_by.first_name} {member.created_by.last_name}".lower()
                agent = agent_lookup.get(user_name)
                
                if not agent:
                    # Try matching just the first name
                    first_name = member.created_by.first_name.lower()
                    agent = agent_lookup.get(first_name)
                
                if agent:
                    if agent.id not in actual_counts:
                        actual_counts[agent.id] = 0
                    actual_counts[agent.id] += 1
                else:
                    unmatched_members.append({
                        'member_id': member.member_id,
                        'user_name': f"{member.created_by.first_name} {member.created_by.last_name}"
                    })
        
        # First reset all counts to 0
        Agent.objects.all().update(farmers_profiled=0)
        
        # Then update each agent's count based on actual assignments
        for agent_id, count in actual_counts.items():
            agent = Agent.objects.get(id=agent_id)
            agent.farmers_profiled = count
            agent.save()
        
        # Print summary
        self.stdout.write(self.style.SUCCESS(f"\nSuccessfully synced farmers_profiled counts"))
        self.stdout.write(f"Total agents: {agents.count()}")
        self.stdout.write(f"Total members: {members.count()}")
        self.stdout.write(f"Members with assigned agents: {sum(actual_counts.values())}")
        self.stdout.write(f"Members without assigned agents: {len(unmatched_members)}")
        
        # Print unmatched members
        if unmatched_members:
            self.stdout.write("\nUnmatched members (first 10):")
            self.stdout.write("-" * 50)
            for member in unmatched_members[:10]:
                self.stdout.write(f"Member ID: {member['member_id']}, User: {member['user_name']}")
            if len(unmatched_members) > 10:
                self.stdout.write(f"... and {len(unmatched_members) - 10} more")
        
        # Print a sample of updated counts
        self.stdout.write("\nSample of updated counts:")
        self.stdout.write("-" * 50)
        for agent_id, count in list(actual_counts.items())[:10]:  # Show first 10 as sample
            agent = Agent.objects.get(id=agent_id)
            self.stdout.write(f"{agent.first_name} {agent.last_name}: {count} members") 