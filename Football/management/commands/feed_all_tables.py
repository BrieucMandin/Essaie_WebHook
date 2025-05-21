"""Custom "master" command calling all table populating commands."""

from django.core.management import call_command
from django.core.management.base import BaseCommand

from Football.constants import TABLE_FEEDING_COMMANDS_LIST


class Command(BaseCommand):
    """
    Commande Django personnalisée pour alimenter toutes les tables de la base de données.

    Cette commande exécute en cascade une liste de commandes individuelles de peuplement
    (définies dans `TABLE_FEEDING_COMMANDS_LIST`) afin de remplir toutes les tables de données
    (par exemple : Joueur, Entraineur, Equipe, etc.).

    Attributs :
        help (str): Message d’aide affiché avec `python manage.py help`.

    Méthodes :
        add_arguments(parser):
            Ajoute une option `--flush` qui permet de supprimer les données de toutes les
            tables avant de les recharger.

        handle(*args, **options):
            Logique principale de la commande :
                - Si l’option `--flush` est fournie, exécute chaque commande avec `--flush` pour
                  réinitialiser les données de toutes les tables.
                - Sinon, exécute simplement les commandes d’alimentation sans suppression préalable.
    """

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
