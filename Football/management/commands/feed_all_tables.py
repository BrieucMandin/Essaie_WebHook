"""Custom "master" command calling all table populating commands."""

from django.core.management import call_command
from django.core.management.base import BaseCommand

from Football.constants import TABLE_FEEDING_COMMANDS_LIST


class Command(BaseCommand):
    """Populate all tables."""

    help = "Enregistre les données dans toutes les tables."

    def add_arguments(self, parser):
        """Command arguments."""

        # Named (optional) arguments.
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Efface au préalable les données de toutes les tables.",
        )

    def handle(self, *args, **options):
        """Command logic."""

        if options["flush"]:
            for table_feeding_command in TABLE_FEEDING_COMMANDS_LIST:
                call_command(table_feeding_command, "--flush")

            return

        for table_feeding_command in TABLE_FEEDING_COMMANDS_LIST:
            call_command(table_feeding_command)
