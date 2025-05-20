from Football.utils import csv_file_path

COMMAND_HELP = "Enregistre les données dans la {table_name}."
COMMAND_FLUSH_OPTION_HELP = "Efface toutes les données de la {table_name}."
SUCCESS_REMOVE_ALL_RECORDS = "Toutes les données de la {table_name} ont été effacées avec succès."
SUCCESS_POPULATE_TABLE = "Les données ont été enregistrées dans la {table_name} avec succès."
ERROR_POPULATE_TABLE = "Une erreur s'est produite lors l'enregistrement des données dans la {table_name}: {error}"


TABLE_JOUEUR_NAME = "Table Joueur"
TABLE_ENTRAINEUR_NAME = "Table Entraineur"
TABLE_EQUIPE_NAME = "Table Equipe"

TABLE_ENTRAINEUR_FILE_PATH = csv_file_path("entraineurs.csv")
TABLE_JOUEUR_FILE_PATH = csv_file_path("joueurs.csv")
TABLE_EQUIPE_FILE_PATH = csv_file_path("equipes.csv")

TABLE_FEEDING_COMMANDS_LIST = [
    "feed_table_joueur",
    "feed_table_entraineur",
    "feed_table_equipe",
]
