from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from Football.models import Joueur, Entraineur, Equipe
from Football.serializers import JoueurSerializer, EntraineurSerializer, EquipeSerializer, EquipeWriteSerializer


class JoueurViewSet(viewsets.ModelViewSet):
    queryset = Joueur.objects.all()
    serializer_class = JoueurSerializer

    def partial_update(self, request, pk=None):
        joueur = self.get_object()
        serializer = JoueurSerializer(joueur, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    @action(detail=False, methods=["get"], url_path="nom/(?P<nom>[^/.]+)")
    def get_by_nom(self, request, nom=None):
        joueurs = Joueur.objects.filter(nom__iexact=nom)
        serializer = self.get_serializer(joueurs, many=True)
        return Response(serializer.data)


class EntraineurViewSet(viewsets.ModelViewSet):
    queryset = Entraineur.objects.all()
    serializer_class = EntraineurSerializer

    @action(detail=False, methods=["get"], url_path="nom/(?P<nom>[^/.]+)")
    def get_by_nom(self, request, nom=None):
        entraineurs = Entraineur.objects.filter(nom__iexact=nom)
        serializer = self.get_serializer(entraineurs, many=True)
        return Response(serializer.data)


class EquipeViewSet(viewsets.ModelViewSet):
    queryset = Equipe.objects.all()

    def get_serializer_class(self):
        if self.request.method in ["POST", "PATCH", "PUT"]:
            return EquipeWriteSerializer
        return EquipeSerializer

    @action(detail=False, methods=["get"], url_path="nom/(?P<nom>[^/.]+)")
    def get_by_nom(self, request, nom=None):
        equipes = Equipe.objects.filter(nom__iexact=nom)
        serializer = self.get_serializer(equipes, many=True)
        return Response(serializer.data)
