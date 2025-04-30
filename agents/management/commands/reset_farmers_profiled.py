from django.core.management.base import BaseCommand
from agents.models import Agent

class Command(BaseCommand):
    help = 'Resets all farmers_profiled counts to zero'

    def handle(self, *args, **options):
        # Get all agents
        agents = Agent.objects.all()
        
        # Reset farmers_profiled count for each agent
        for agent in agents:
            agent.farmers_profiled = 0
            agent.save()
        
        self.stdout.write(self.style.SUCCESS(f'Successfully reset farmers_profiled count for {agents.count()} agents')) 