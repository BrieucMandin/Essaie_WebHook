from unittest.mock import patch

from django.db import transaction
from django.test import TransactionTestCase


from Football.models import Joueur, Entraineur, Equipe


class TestWebhookSignals(TransactionTestCase):

    @patch("Football.signals.requests.post")
    def test_post_save_joueur_triggers_webhook(self, mock_post):

        joueur = Joueur.objects.create(
            id_J=1, nom="Mbappé", age=25, poste="ATT", nationalite="Française", pied_fort="D", nombre_but=300
        )
        transaction.commit()
        self.assertTrue(mock_post.called)
        payload = {"id": joueur.id_J, "nom": joueur.nom, "type": "joueur", "action": "update"}
        mock_post.assert_called_with("http://127.0.0.1:8080/webhook-endpoint/", json=payload)

    @patch("Football.signals.requests.post")
    def test_post_delete_joueur_triggers_webhook(self, mock_post):

        joueur = Joueur.objects.create(
            id_J=2, nom="Griezmann", age=33, poste="MID", nationalite="Française", pied_fort="G", nombre_but=200
        )
        payload = {"id": joueur.id_J, "nom": joueur.nom, "type": "joueur", "action": "delete"}
        joueur.delete()
        self.assertTrue(mock_post.called)
        mock_post.assert_called_with("http://127.0.0.1:8080/webhook-endpoint/", json=payload)

    @patch("Football.signals.requests.post")
    def test_post_save_entraineur_triggers_webhook(self, mock_post):

        entraineur = Entraineur.objects.create(id_En=1, nom="Deschamps", experience=10, nationalite="Française")
        transaction.commit()
        self.assertTrue(mock_post.called)
        payload = {"id": entraineur.id_En, "nom": entraineur.nom, "type": "entraineur", "action": "update"}
        mock_post.assert_called_with("http://127.0.0.1:8080/webhook-endpoint/", json=payload)

    @patch("Football.signals.requests.post")
    def test_post_delete_entraineur_triggers_webhook(self, mock_post):

        entraineur = Entraineur.objects.create(id_En=2, nom="Zidane", experience=7, nationalite="Française")
        payload = {"id": entraineur.id_En, "nom": entraineur.nom, "type": "entraineur", "action": "delete"}
        entraineur.delete()

        self.assertTrue(mock_post.called)
        mock_post.assert_called_with("http://127.0.0.1:8080/webhook-endpoint/", json=payload)

    @patch("Football.signals.requests.post")
    def test_m2m_changed_equipe_triggers_webhook(self, mock_post):

        entraineur = Entraineur.objects.create(id_En=3, nom="Henry", experience=3, nationalite="Française")
        equipe = Equipe.objects.create(id_Eq=1, nom="Bleus", stade="Stade de France", entraineur=entraineur)
        joueur = Joueur.objects.create(
            id_J=3, nom="Thuram", age=26, poste="ATT", nationalite="Française", pied_fort="D", nombre_but=20
        )
        equipe.joueurs.add(joueur)
        transaction.commit()
        self.assertTrue(mock_post.called)
        payload = {"id": equipe.id_Eq, "nom": equipe.nom, "type": "equipe", "action": "update"}
        mock_post.assert_called_with("http://127.0.0.1:8080/webhook-endpoint/", json=payload)

    @patch("Football.signals.requests.post")
    def test_post_delete_equipe_triggers_webhook(self, mock_post):

        entraineur = Entraineur.objects.create(id_En=4, nom="Blanc", experience=5, nationalite="Française")
        equipe = Equipe.objects.create(id_Eq=2, nom="Reds", stade="Old Trafford", entraineur=entraineur)
        payload = {"id": equipe.id_Eq, "nom": equipe.nom, "type": "equipe", "action": "delete"}
        equipe.delete()  # <-- important : déclenche le signal post_delete
        self.assertTrue(mock_post.called)
        mock_post.assert_called_with("http://127.0.0.1:8080/webhook-endpoint/", json=payload)
