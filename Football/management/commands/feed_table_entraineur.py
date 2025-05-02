import csv

from django.core.management.base import BaseCommand
from Football.models import Entraineur
from Football.constants import (
    COMMAND_FLUSH_OPTION_HELP,
    COMMAND_HELP,
    ERROR_POPULATE_TABLE,
    SUCCESS_POPULATE_TABLE,
    SUCCESS_REMOVE_ALL_RECORDS,
    TABLE_ENTRAINEUR_FILE_PATH,
    TABLE_ENTRAINEUR_NAME,
)
from Football.utils import detect_encoding


class Command(BaseCommand):
    """Populate the Entraineur table."""

    help = COMMAND_HELP.format(table_name=TABLE_ENTRAINEUR_NAME)

    def add_arguments(self, parser):
        """Command arguments."""

        # Named (optional) arguments.
        parser.add_argument(
            "--flush",
            action="store_true",
            help=COMMAND_FLUSH_OPTION_HELP.format(table_name=TABLE_ENTRAINEUR_NAME),
        )

    def handle(self, *args, **options):
        """Command logic."""

        if options["flush"]:
            Entraineur.objects.all().delete()
            self.stdout.write(self.style.SUCCESS(SUCCESS_REMOVE_ALL_RECORDS.format(table_name=TABLE_ENTRAINEUR_NAME)))

        try:
            with open(TABLE_ENTRAINEUR_FILE_PATH, newline="", encoding=detect_encoding(TABLE_ENTRAINEUR_FILE_PATH)) as csv_file:
                table_reader = csv.reader(csv_file, delimiter=",")
                next(table_reader)  # Skip first row containing column names.
                for row in table_reader:
                    nom = row[0]
                    experience = int(row[1])
                    nationalite = row[2]
                    id = int(row[3])

                    # Création ou mise à jour de l'entraîneur dans la base de données
                    Entraineur.objects.update_or_create(
                        id_En=id,
                        nom=nom,
                        defaults={
                            "experience": experience,
                            "nationalite": nationalite,
                        },
                    )

                self.stdout.write(self.style.SUCCESS(SUCCESS_POPULATE_TABLE.format(table_name=TABLE_ENTRAINEUR_NAME)))

        except Exception as error:
            self.stderr.write(self.style.ERROR(ERROR_POPULATE_TABLE.format(table_name=TABLE_ENTRAINEUR_NAME, error=error)))
