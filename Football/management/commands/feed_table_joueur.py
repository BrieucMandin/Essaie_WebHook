import csv

from django.core.management.base import BaseCommand
from Football.models import Joueur
from Football.constants import (
    COMMAND_FLUSH_OPTION_HELP,
    COMMAND_HELP,
    ERROR_POPULATE_TABLE,
    SUCCESS_POPULATE_TABLE,
    SUCCESS_REMOVE_ALL_RECORDS,
    TABLE_JOUEUR_FILE_PATH,
    TABLE_JOUEUR_NAME,
)
from Football.utils import detect_encoding


class Command(BaseCommand):
    """
    Commande Django personnalisée pour alimenter la table ``Joueur``.

    Cette commande lit un fichier CSV contenant les données des joueurs
    et les insère ou les met à jour dans la base de données. Elle propose
    également une option ``--flush`` pour vider la table avant insertion.

    Attributs :
        help (str): Description de l'aide affichée avec ``python manage.py help``.

    Méthodes :
        add_arguments(parser):
            Ajoute l'option ``--flush`` à la commande pour vider la table ``Joueur`` avant l'importation.

        La méthode ``handle(*args, **options)``

            Exécute la logique principale de la commande :

            - Vide la table si l'option ``--flush`` est utilisée.
            - Lit le fichier CSV à l'emplacement ``TABLE_JOUEUR_FILE_PATH``.
            - Pour chaque ligne, insère ou met à jour un objet ``Joueur``.
            - Affiche un message de succès ou d'erreur.
    """


    help = COMMAND_HELP.format(table_name=TABLE_JOUEUR_NAME)

    def add_arguments(self, parser):
        """Command arguments."""

        # Named (optional) arguments.
        parser.add_argument(
            "--flush",
            action="store_true",
            help=COMMAND_FLUSH_OPTION_HELP.format(table_name=TABLE_JOUEUR_NAME),
        )

    def handle(self, *args, **options):
        """Command logic."""

        if options["flush"]:
            Joueur.objects.all().delete()
            self.stdout.write(self.style.SUCCESS(SUCCESS_REMOVE_ALL_RECORDS.format(table_name=TABLE_JOUEUR_NAME)))

        try:
            with open(TABLE_JOUEUR_FILE_PATH, newline="", encoding=detect_encoding(TABLE_JOUEUR_FILE_PATH)) as csv_file:
                table_reader = csv.reader(csv_file, delimiter=",")
                next(table_reader)  # Skip first row containing column names.
                for row in table_reader:
                    nom = row[0]
                    age = int(row[1])
                    poste = row[2]
                    nationalite = row[3]
                    pied_fort = row[4]
                    nombre_but = int(row[5])
                    id = int(row[6])

                    # Création ou mise à jour du joueur dans la base de données
                    Joueur.objects.update_or_create(
                        id_J=id,
                        nom=nom,
                        defaults={
                            "age": age,
                            "poste": poste,
                            "nationalite": nationalite,
                            "pied_fort": pied_fort,
                            "nombre_but": nombre_but,
                        },
                    )

                self.stdout.write(self.style.SUCCESS(SUCCESS_POPULATE_TABLE.format(table_name=TABLE_JOUEUR_NAME)))

        except Exception as error:
            self.stderr.write(self.style.ERROR(ERROR_POPULATE_TABLE.format(table_name=TABLE_JOUEUR_NAME, error=error)))
