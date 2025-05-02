from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from Football.models import Joueur, Entraineur, Equipe


class ViewSetCommonTestsMixin:
    model = None
    nom = None
    url_list_name = None
    url_detail_name = None
    url_get_by_nom_name = None

    def get_detail_url(self):
        return reverse(self.url_detail_name, args=[self.obj.pk])

    def get_by_nom_url(self):
        return reverse(self.url_get_by_nom_name, args=[self.nom])

    def test_list(self):
        response = self.client.get(reverse(self.url_list_name))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_by_nom(self):
        url = self.get_by_nom_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['nom'], self.nom)


class JoueurViewSetTest(ViewSetCommonTestsMixin, APITestCase):

    def setUp(self):
        self.nom = "Kylian Mbappé"
        self.obj = Joueur.objects.create(
            id_J = 1, nom=self.nom, age=25, poste="ATT", nationalite="France",
            pied_fort="D", nombre_but=40
        )
        self.url_list_name = 'joueur-list'
        self.url_detail_name = 'joueur-detail'
        self.url_get_by_nom_name = 'joueur-get-by-nom'

    def test_partial_update(self):
        url = self.get_detail_url()
        response = self.client.patch(url, {'age': 26})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['age'], 26)


class EntraineurViewSetTest(ViewSetCommonTestsMixin, APITestCase):

    def setUp(self):
        self.nom = "Deschamps"
        self.obj = Entraineur.objects.create(
            nom=self.nom,
            experience=10,
            nationalite="France"
        )
        self.url_list_name = 'entraineur-list'
        self.url_detail_name = 'entraineur-detail'
        self.url_get_by_nom_name = 'entraineur-get-by-nom'


class EquipeViewSetTest(ViewSetCommonTestsMixin, APITestCase):
    def setUp(self):
        self.nom = "France FC"

        entraineur = Entraineur(
            id_En=1,
            nom="Deschamps",
            experience=10,
            nationalite="France"
        )
        entraineur.save()  # Séparation explicite
        assert entraineur.pk is not None  # Vérifie qu'il a été sauvegardé

        self.obj = Equipe.objects.create(
            nom=self.nom,
            stade="Stade de France",
            entraineur=entraineur
        )

        self.url_list_name = 'equipe-list'
        self.url_detail_name = 'equipe-detail'
        self.url_get_by_nom_name = 'equipe-get-by-nom'
