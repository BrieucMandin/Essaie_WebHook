from rest_framework import serializers
from .models import Joueur, Entraineur, Equipe


class JoueurSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le modèle :class:`Joueur`.

    Sérialise tous les champs du modèle `Joueur`.

    :Meta:
        model: :class:`Joueur`
        fields: "__all__" – tous les champs du modèle sont inclus.
    """

    class Meta:
        model = Joueur
        fields = "__all__"


class EntraineurSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le modèle :class:`Entraineur`.

    Sérialise tous les champs du modèle `Entraineur`.

    :Meta:
        model: :class:`Entraineur`
        fields: "__all__" – tous les champs du modèle sont inclus.
    """

    class Meta:
        model = Entraineur
        fields = "__all__"


class EquipeSerializer(serializers.ModelSerializer):
    """
    Sérialiseur en lecture pour le modèle :class:`Equipe`.

    Utilise des sérialiseurs imbriqués pour afficher les détails de l'entraîneur
    et des joueurs associés.

    :cvar entraineur: Sérialiseur imbriqué pour l'entraîneur.
    :type entraineur: EntraineurSerializer

    :cvar joueurs: Sérialiseur imbriqué pour les joueurs.
    :type joueurs: JoueurSerializer (many=True)

    :Meta:
        model: :class:`Equipe`
        fields: Liste explicite des champs à inclure : "id_Eq", "nom", "stade", "entraineur", "joueurs".
    """

    entraineur = EntraineurSerializer()
    joueurs = JoueurSerializer(many=True)

    class Meta:
        model = Equipe
        fields = ["id_Eq", "nom", "stade", "entraineur", "joueurs"]


class EquipeWriteSerializer(serializers.ModelSerializer):
    """
    Sérialiseur en écriture pour le modèle :class:`Equipe`.

    Utilise des champs `PrimaryKeyRelatedField` pour l'entraîneur et les joueurs,
    permettant la création ou mise à jour d’une équipe à partir de leurs identifiants.

    :cvar entraineur: Champ de relation pour l'entraîneur (clé primaire).
    :type entraineur: serializers.PrimaryKeyRelatedField

    :cvar joueurs: Champ de relation multiple pour les joueurs (clés primaires).
    :type joueurs: serializers.PrimaryKeyRelatedField (many=True)

    :Meta:
        model: :class:`Equipe`
        fields: "__all__" – tous les champs du modèle sont inclus.
    """

    entraineur = serializers.PrimaryKeyRelatedField(queryset=Entraineur.objects.all())
    joueurs = serializers.PrimaryKeyRelatedField(queryset=Joueur.objects.all(), many=True)

    class Meta:
        model = Equipe
        fields = "__all__"
