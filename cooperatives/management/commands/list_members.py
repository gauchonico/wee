from django.core.management.base import BaseCommand
from cooperatives.models import Member

class Command(BaseCommand):
    help = 'Show details for a single member by their system_id'

    def add_arguments(self, parser):
        parser.add_argument('system_id', type=str, help='The system_id to look up')

    def handle(self, *args, **options):
        system_id = options['system_id']
        
        try:
            member = Member.objects.select_related(
                'cooperative', 'farmer_group', 'district', 'county', 
                'sub_county', 'village', 'created_by'
            ).get(system_id=system_id)
            
            self.stdout.write(self.style.SUCCESS(f"\nMember Details for System ID: {member.system_id}"))
            self.stdout.write("=" * 80)
            self.stdout.write(f"Member ID: {member.member_id}")
            self.stdout.write(f"Name: {member.first_name} {member.surname}")
            self.stdout.write(f"Other Name: {member.other_name or 'N/A'}")
            self.stdout.write(f"Phone: {member.phone_number}")
            self.stdout.write(f"Email: {member.email or 'N/A'}")
            self.stdout.write(f"Gender: {member.gender}")
            self.stdout.write(f"ID Number: {member.id_number}")
            self.stdout.write(f"Date of Birth: {member.date_of_birth or 'N/A'}")
            self.stdout.write(f"Role: {member.role}")
            self.stdout.write(f"Cooperative: {member.cooperative.fpo_name if member.cooperative else 'N/A'}")
            self.stdout.write(f"Farmer Group: {member.farmer_group.name if member.farmer_group else 'N/A'}")
            self.stdout.write(f"District: {member.district.name if member.district else 'N/A'}")
            self.stdout.write(f"County: {member.county.name if member.county else 'N/A'}")
            self.stdout.write(f"Sub County: {member.sub_county.name if member.sub_county else 'N/A'}")
            self.stdout.write(f"Village: {member.village.name if member.village else 'N/A'}")
            self.stdout.write(f"GPS Coordinates: {member.gps_coordinates or 'N/A'}")
            self.stdout.write(f"Land Acres: {member.land_acres or 0}")
            self.stdout.write(f"Shea Trees: {member.shea_trees or 0}")
            self.stdout.write(f"Beehives: {member.beehives or 0}")
            self.stdout.write(f"Created At: {member.created_at}")
            self.stdout.write(f"Created By: {member.created_by.username if member.created_by else 'N/A'}")
            
            # Show products
            products = member.products.all()
            if products:
                self.stdout.write("\nProducts:")
                for product in products:
                    self.stdout.write(f"- {product.name}")
            else:
                self.stdout.write("\nNo products assigned")
            
            self.stdout.write("=" * 80)
            
        except Member.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Member with System ID {system_id} not found')) 