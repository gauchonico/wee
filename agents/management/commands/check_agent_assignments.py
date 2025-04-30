from django.core.management.base import BaseCommand
from agents.models import Agent
from cooperatives.models import Member
from django.contrib.auth.models import User
from django.db.models import Count

class Command(BaseCommand):
    help = 'Checks agent assignments and member counts'

    def handle(self, *args, **options):
        # Get all agents
        agents = Agent.objects.all()
        
        # Get all members with their created_by information
        members = Member.objects.select_related('created_by').all()
        
        # Create a dictionary to store actual member counts
        actual_counts = {}
        for member in members:
            if member.created_by:
                # Find the agent for this user
                agent = Agent.objects.filter(
                    first_name__iexact=member.created_by.first_name,
                    last_name__iexact=member.created_by.last_name
                ).first()
                if agent:
                    if agent.id not in actual_counts:
                        actual_counts[agent.id] = 0
                    actual_counts[agent.id] += 1
        
        # Print header
        self.stdout.write("\nAgent Assignments Report:")
        self.stdout.write("-" * 80)
        self.stdout.write(f"{'Agent Name':<30} {'Farmers Profiled':<15} {'Actual Count':<15} {'Difference':<15}")
        self.stdout.write("-" * 80)
        
        # Print each agent's information
        for agent in agents:
            actual_count = actual_counts.get(agent.id, 0)
            difference = agent.farmers_profiled - actual_count
            self.stdout.write(
                f"{agent.first_name + ' ' + agent.last_name:<30} "
                f"{agent.farmers_profiled:<15} "
                f"{actual_count:<15} "
                f"{difference:<15}"
            )
        
        # Print summary
        self.stdout.write("-" * 80)
        self.stdout.write(f"Total agents: {agents.count()}")
        self.stdout.write(f"Total members: {members.count()}")
        self.stdout.write(f"Members with assigned agents: {sum(actual_counts.values())}")
        self.stdout.write(f"Members without assigned agents: {members.count() - sum(actual_counts.values())}") 