from rest_framework import serializers
from .models import Joueur, Entraineur, Equipe


class JoueurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Joueur
        fields = '__all__'


class EntraineurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entraineur
        fields = '__all__'


class EquipeSerializer(serializers.ModelSerializer):
    entraineur = EntraineurSerializer()
    joueurs = JoueurSerializer(many=True)

    class Meta:
        model = Equipe
        fields = ['id','nom', 'stade', 'joueurs', 'entraineur'] 


class EquipeWriteSerializer(serializers.ModelSerializer):
    entraineur = serializers.PrimaryKeyRelatedField(queryset=Entraineur.objects.all())
    joueurs = serializers.PrimaryKeyRelatedField(queryset=Joueur.objects.all(), many=True)

    class Meta:
        model = Equipe
        fields = '__all__'
