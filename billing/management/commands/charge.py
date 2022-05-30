from django.core.management import BaseCommand
from billing.services import OrganizationReportCreator


class Command(BaseCommand):
    help = 'Charging and Create reports'

    def handle(self, *args, **options):
        OrganizationReportCreator.run()
        self.stdout.write(self.style.SUCCESS("Successfully charged"))
