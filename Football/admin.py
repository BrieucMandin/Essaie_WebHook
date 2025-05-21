from django.contrib import admin

from .models import Joueur, Entraineur, Equipe


class JoueurAdmin(admin.ModelAdmin):
    """
    Interface d'administration pour le modèle :class:`Joueur`.

    Permet de personnaliser l'affichage, la recherche et les filtres disponibles
    dans l'interface d'administration Django.

    :cvar list_display: Liste des champs affichés dans la vue liste.
    :type list_display: tuple(str)

    :cvar search_fields: Champs sur lesquels la recherche est autorisée.
    :type search_fields: tuple(str)

    :cvar list_filter: Champs disponibles pour filtrer la liste.
    :type list_filter: tuple(str)
    """

    list_display = (
        "id_J",
        "nom",
        "age",
        "poste",
        "nationalite",
        "pied_fort",
        "nombre_but",
    )  # Champs à afficher dans la liste
    search_fields = ("nom", "poste", "nationalite")  # Champs qui peuvent être recherchés
    list_filter = ("poste", "pied_fort")  # Filtres à gauche dans l'interface


# Personnalisation de l'affichage du modèle Entraineur
class EntraineurAdmin(admin.ModelAdmin):
    """
    Interface d'administration pour le modèle :class:`Entraineur`.

    Affiche les informations clés de l'entraîneur et permet la recherche dans l'admin Django.

    :cvar list_display: Champs visibles dans la vue liste.
    :type list_display: tuple(str)

    :cvar search_fields: Champs indexés pour la recherche.
    :type search_fields: tuple(str)
    """

    list_display = ("id_En", "nom", "experience", "nationalite")  # Champs à afficher dans la liste
    search_fields = ("nom", "nationalite")  # Champs qui peuvent être recherchés


# Personnalisation de l'affichage du modèle Equipe
class EquipeAdmin(admin.ModelAdmin):
    """
    Interface d'administration pour le modèle :class:`Equipe`.

    Personnalise la présentation des équipes dans l'interface d'administration,
    incluant l'affichage des joueurs associés.

    :cvar list_display: Champs affichés dans la vue liste.
    :type list_display: tuple(str)

    :cvar search_fields: Champs sur lesquels la recherche est activée.
    :type search_fields: tuple(str)

    :cvar joueurs_list: Méthode utilitaire pour afficher les noms des joueurs dans la liste des équipes.
    """

    list_display = ("id_Eq", "nom", "stade", "entraineur", "joueurs_list")  # Champs à afficher dans la liste
    search_fields = ("nom", "stade")  # Champs qui peuvent être recherchés

    def joueurs_list(self, obj):
        """
        Retourne une chaîne contenant les noms des joueurs de l’équipe, séparés par des virgules.

        :param obj: Instance du modèle :class:`Equipe`
        :type obj: Equipe
        :return: Liste des noms des joueurs sous forme de chaîne
        :rtype: str
        """
        return ", ".join([joueur.nom for joueur in obj.joueurs.all()])

    joueurs_list.short_description = "Joueurs"  # Nom de la colonne dans l'admin


admin.site.register(Joueur, JoueurAdmin)
admin.site.register(Entraineur, EntraineurAdmin)
admin.site.register(Equipe, EquipeAdmin)
