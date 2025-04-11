from django.core.management.base import BaseCommand
from cooperatives.models import Member

class Command(BaseCommand):
    help = 'Updates existing member records to set is_verified and has_mobile_money to True, and id_type to national_id where id_number exists'

    def handle(self, *args, **options):
        # Update all members to set is_verified and has_mobile_money to True
        updated_count = Member.objects.all().update(
            is_verified=True,
            has_mobile_money=True
        )
        self.stdout.write(self.style.SUCCESS(f'Updated {updated_count} members with is_verified and has_mobile_money set to True'))

        # Update members with id_number to set id_type to national_id
        members_with_id = Member.objects.filter(id_number__isnull=False, id_type__isnull=True)
        id_updated_count = members_with_id.update(id_type='national_id')
        self.stdout.write(self.style.SUCCESS(f'Updated {id_updated_count} members with id_number to set id_type to national_id')) 