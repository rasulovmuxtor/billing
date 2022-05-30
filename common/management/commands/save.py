from django.core.management import BaseCommand
from common.factory import OrganizationFactory


class Command(BaseCommand):
    help = 'Created dummy data'

    def handle(self, *args, **options):
        OrganizationFactory.create_batch(3)
        self.stdout.write(self.style.SUCCESS("Successfully saved dummy data"))
