from django.core.management.base import BaseCommand
from cooperatives.models import Member
from django.contrib.auth.models import User
from django.db.models import Count

class Command(BaseCommand):
    help = 'Shows current member-agent assignments'

    def handle(self, *args, **options):
        # Get all members with their created_by information
        members = Member.objects.select_related('created_by').all()
        
        # Group members by their created_by user
        user_counts = {}
        for member in members:
            if member.created_by:
                user_key = f"{member.created_by.first_name} {member.created_by.last_name}"
                if user_key not in user_counts:
                    user_counts[user_key] = 0
                user_counts[user_key] += 1
        
        self.stdout.write("\nCurrent Member Assignments:")
        self.stdout.write("-" * 80)
        self.stdout.write(f"{'User Name':<40} {'Member Count':<15}")
        self.stdout.write("-" * 80)
        
        for user_name, count in sorted(user_counts.items(), key=lambda x: x[1], reverse=True):
            self.stdout.write(f"{user_name:<40} {count:<15}")
        
        self.stdout.write("-" * 80)
        self.stdout.write(f"Total members: {members.count()}")
        self.stdout.write(f"Members with assigned users: {sum(user_counts.values())}")
        self.stdout.write(f"Members without assigned users: {members.count() - sum(user_counts.values())}") 