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
    """
    Commande Django personnalisée pour alimenter la table `Equipe`.

    Cette commande lit un fichier CSV contenant les données des équipes,
    leurs entraîneurs et les joueurs associés. Elle insère ou met à jour
    les enregistrements dans la base de données, tout en gérant les
    relations de type ForeignKey et ManyToMany.

    Attributs :
        help (str): Message d’aide affiché avec la commande `python manage.py help`.

    Méthodes :
        add_arguments(parser):
            Ajoute une option `--flush` permettant de supprimer tous les
            enregistrements existants dans la table `Equipe` avant l’import.

        handle(*args, **options):
            Logique principale de la commande :
                - Supprime les enregistrements si l’option `--flush` est utilisée.
                - Ouvre et lit le fichier `TABLE_EQUIPE_FILE_PATH`.
                - Pour chaque ligne :
                    - Récupère les données de l'équipe (nom, stade, entraîneur, joueurs, id).
                    - Recherche l'entraîneur et les joueurs associés.
                    - Crée ou met à jour une instance `Equipe`.
                    - Met à jour la relation ManyToMany avec les joueurs.
                - Affiche un message de succès ou une erreur selon le résultat.
    """

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
                    id = int(row[4])

                    # Trouver l'entraîneur
                    entraineur = Entraineur.objects.get(id_En=entraineur_id)

                    # Trouver les joueurs
                    joueurs = Joueur.objects.filter(id_J__in=joueurs_ids)

                    # Créer ou mettre à jour l'équipe
                    equipe, created = Equipe.objects.update_or_create(
                        id_Eq=id,
                        defaults={
                            "nom": nom,
                            "stade": stade,
                            "entraineur": entraineur,
                        },
                    )

                    # Mettre à jour la relation ManyToMany avec les joueurs
                    equipe.joueurs.set(joueurs)

                self.stdout.write(self.style.SUCCESS(SUCCESS_POPULATE_TABLE.format(table_name=TABLE_EQUIPE_NAME)))

        except Exception as error:
            self.stderr.write(self.style.ERROR(ERROR_POPULATE_TABLE.format(table_name=TABLE_EQUIPE_NAME, error=error)))
