import csv

from django.core.management.base import BaseCommand
from Football.models import Equipe, Entraineur, Joueur
from Football.constants import (
    COMMAND_FLUSH_OPTION_HELP,
    COMMAND_HELP,
    ERROR_POPULATE_TABLE,
    SUCCESS_POPULATE_TABLE,
    SUCCESS_REMOVE_ALL_RECORDS,
    TABLE_EQUIPE_FILE_PATH,
    TABLE_EQUIPE_NAME,
)
from Football.utils import detect_encoding


class Command(BaseCommand):
    """Populate the Equipe table."""

    help = COMMAND_HELP.format(table_name=TABLE_EQUIPE_NAME)

    def add_arguments(self, parser):
        """Command arguments."""

        # Named (optional) arguments.
        parser.add_argument(
            "--flush",
            action="store_true",
            help=COMMAND_FLUSH_OPTION_HELP.format(table_name=TABLE_EQUIPE_NAME),
        )

    def handle(self, *args, **options):
        """Command logic."""

        if options["flush"]:
            Equipe.objects.all().delete()
            self.stdout.write(self.style.SUCCESS(SUCCESS_REMOVE_ALL_RECORDS.format(table_name=TABLE_EQUIPE_NAME)))

        try:
            with open(TABLE_EQUIPE_FILE_PATH, newline="", encoding=detect_encoding(TABLE_EQUIPE_FILE_PATH)) as csv_file:
                table_reader = csv.reader(csv_file, delimiter=",")
                next(table_reader)  # Skip first row containing column names.
                for row in table_reader:
                    nom = row[0]
                    stade = row[1]
                    entraineur_id = int(row[2])  # ID de l'entraîneur
                    joueurs_ids = list(map(int, row[3].split(";")))  # Liste d'IDs des joueurs

                    # Trouver l'entraîneur
                    entraineur = Entraineur.objects.get(id=entraineur_id)

                    # Trouver les joueurs
                    joueurs = Joueur.objects.filter(id__in=joueurs_ids)

                    # Créer ou mettre à jour l'équipe
                    equipe, created = Equipe.objects.update_or_create(
                        nom=nom,
                        defaults={
                            "stade": stade,
                            "entraineur": entraineur,
                        },
                    )

                    # Mettre à jour la relation ManyToMany avec les joueurs
                    equipe.joueurs.set(joueurs)

                self.stdout.write(self.style.SUCCESS(SUCCESS_POPULATE_TABLE.format(table_name=TABLE_EQUIPE_NAME)))

        except Exception as error:
            self.stderr.write(self.style.ERROR(ERROR_POPULATE_TABLE.format(table_name=TABLE_EQUIPE_NAME, error=error)))
