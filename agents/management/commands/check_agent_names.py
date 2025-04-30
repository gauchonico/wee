from django.core.management.base import BaseCommand
from agents.models import Agent
import csv
from datetime import datetime

class Command(BaseCommand):
    help = 'Display all agent names in the database and save to CSV'

    def handle(self, *args, **options):
        agents = Agent.objects.all().order_by('first_name', 'last_name')
        
        if not agents.exists():
            self.stdout.write(self.style.WARNING('No agents found in the database.'))
            return
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'agent_list_{timestamp}.csv'
        
        # Write to CSV
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            # Write header
            writer.writerow(['ID', 'First Name', 'Last Name', 'Farmers Profiled'])
            
            # Write data
            for agent in agents:
                writer.writerow([
                    agent.id,
                    agent.first_name,
                    agent.last_name,
                    agent.farmers_profiled
                ])
        
        # Display summary
        self.stdout.write(self.style.SUCCESS(f'Agent list has been saved to {filename}'))
        self.stdout.write(self.style.SUCCESS(f'Total agents: {agents.count()}'))
        
        # Display the first few rows as a preview
        self.stdout.write('\nPreview of the CSV file:')
        self.stdout.write('-' * 50)
        self.stdout.write(f"{'ID':<5} {'First Name':<15} {'Last Name':<15} {'Farmers Profiled':<15}")
        self.stdout.write('-' * 50)
        for agent in agents[:5]:  # Show first 5 agents as preview
            self.stdout.write(f"{agent.id:<5} {agent.first_name:<15} {agent.last_name:<15} {agent.farmers_profiled:<15}")
        if agents.count() > 5:
            self.stdout.write('...') 