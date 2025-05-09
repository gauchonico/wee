from django.core.management.base import BaseCommand
from cooperatives.models import Member

class Command(BaseCommand):
    help = 'Check member IDs in the database'

    def add_arguments(self, parser):
        parser.add_argument('--member_ids', nargs='+', type=str, help='List of member IDs to check')

    def handle(self, *args, **options):
        member_ids = options.get('member_ids', [])
        
        if member_ids:
            members = Member.objects.filter(member_id__in=member_ids)
            self.stdout.write(f"\nChecking for members with IDs: {', '.join(member_ids)}")
        else:
            members = Member.objects.all()
            self.stdout.write("\nListing all members in the database:")

        if not members.exists():
            self.stdout.write(self.style.WARNING("No members found!"))
            return

        for member in members:
            self.stdout.write(
                f"Member ID: {member.member_id}\n"
                f"Name: {member.first_name} {member.surname}\n"
                f"Phone: {member.phone_number}\n"
                f"Cooperative: {member.cooperative.fpo_name if member.cooperative else 'None'}\n"
                f"Created at: {member.created_at}\n"
                f"{'='*50}"
            ) 