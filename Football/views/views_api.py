from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from Football.models import Joueur, Entraineur, Equipe
from Football.serializers import JoueurSerializer, EntraineurSerializer, EquipeSerializer, EquipeWriteSerializer


class JoueurViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour gérer les joueurs.

    Fournit les opérations CRUD classiques (création, lecture, mise à jour, suppression)
    ainsi qu'une action personnalisée pour rechercher des joueurs par nom.

    Méthodes supplémentaires :
    - partial_update : mise à jour partielle d'un joueur.
    - get_by_nom : recherche de joueurs par nom (insensible à la casse).

    Attributs :
        queryset (QuerySet): Ensemble des joueurs.
        serializer_class (Serializer): Sérialiseur utilisé pour les joueurs.
    """

    queryset = Joueur.objects.all()
    serializer_class = JoueurSerializer

    def partial_update(self, request, pk=None):
        """
        Effectue une mise à jour partielle d'un joueur.

        Args:
            request (Request): La requête HTTP contenant les données à mettre à jour.
            pk (int, optional): Identifiant du joueur.

        Returns:
            Response: Données du joueur mises à jour en cas de succès, sinon erreurs de validation.
        """

        joueur = self.get_object()
        serializer = JoueurSerializer(joueur, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    @action(detail=False, methods=["get"], url_path="nom/(?P<nom>[^/.]+)")
    def get_by_nom(self, request, nom=None):
        """
        Recherche et retourne la liste des joueurs correspondant exactement au nom donné.

        Args:
            request (Request): La requête HTTP.
            nom (str): Nom du joueur à rechercher (insensible à la casse).

        Returns:
            Response: Liste des joueurs correspondants sérialisés.
        """

        joueurs = Joueur.objects.filter(nom__iexact=nom)
        serializer = self.get_serializer(joueurs, many=True)
        return Response(serializer.data)


class EntraineurViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour gérer les entraîneurs.

    Fournit les opérations CRUD classiques
    ainsi qu'une action personnalisée pour rechercher des entraîneurs par nom.

    Attributs :
        queryset (QuerySet): Ensemble des entraîneurs.
        serializer_class (Serializer): Sérialiseur utilisé pour les entraîneurs.
    """

    queryset = Entraineur.objects.all()
    serializer_class = EntraineurSerializer

    @action(detail=False, methods=["get"], url_path="nom/(?P<nom>[^/.]+)")
    def get_by_nom(self, request, nom=None):
        """
        Recherche et retourne la liste des entraîneurs correspondant exactement au nom donné.

        Args:
            request (Request): La requête HTTP.
            nom (str): Nom de l'entraîneur à rechercher (insensible à la casse).

        Returns:
            Response: Liste des entraîneurs correspondants sérialisés.
        """

        entraineurs = Entraineur.objects.filter(nom__iexact=nom)
        serializer = self.get_serializer(entraineurs, many=True)
        return Response(serializer.data)


class EquipeViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour gérer les équipes.

    Fournit les opérations CRUD classiques avec une gestion différente des serializers
    selon le type de requête (lecture ou écriture),
    ainsi qu'une action personnalisée pour rechercher des équipes par nom.

    Attributs :
        queryset (QuerySet): Ensemble des équipes.
    """

    queryset = Equipe.objects.all()

    def get_serializer_class(self):
        """
        Retourne le serializer approprié en fonction de la méthode HTTP de la requête.

        - Pour les méthodes POST, PATCH et PUT, utilise `EquipeWriteSerializer` pour l'écriture.
        - Pour les autres méthodes (GET), utilise `EquipeSerializer` pour la lecture.

        Returns:
            Serializer: Classe du serializer à utiliser.
        """

        if self.request.method in ["POST", "PATCH", "PUT"]:
            return EquipeWriteSerializer
        return EquipeSerializer

    @action(detail=False, methods=["get"], url_path="nom/(?P<nom>[^/.]+)")
    def get_by_nom(self, request, nom=None):
        """
        Recherche et retourne la liste des équipes correspondant exactement au nom donné.

        Args:
            request (Request): La requête HTTP.
            nom (str): Nom de l'équipe à rechercher (insensible à la casse).

        Returns:
            Response: Liste des équipes correspondantes sérialisées.
        """

        equipes = Equipe.objects.filter(nom__iexact=nom)
        serializer = self.get_serializer(equipes, many=True)
        return Response(serializer.data)
