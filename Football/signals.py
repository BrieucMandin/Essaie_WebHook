# ton_app/signals.py
import requests
import time

from django.db.models.signals import post_delete, post_save, m2m_changed
from django.db import transaction
from django.dispatch import receiver

from .models import Joueur, Entraineur, Equipe


@receiver(post_save, sender=Joueur)
def notify_webhook_receiver_Joueur(sender, instance, created, **kwargs):

    def send_webhook():

        payload = {"id": instance.id_J, "nom": instance.nom, "type": "joueur", "action": "update"}
        try:
            requests.post("http://127.0.0.1:8080/webhook-endpoint/", json=payload)
            print(f"🚨 Post envoyée pour le joueur {instance.nom}")
        except requests.RequestException as e:
            print("Erreur webhook :", e)

    # Exécuter seulement après commit de la transaction
    transaction.on_commit(send_webhook)


@receiver(post_delete, sender=Joueur)
def notify_webhook_delete_Joueur(sender, instance, **kwargs):
    def send_webhook():

        payload = {"id": instance.id_J, "nom": instance.nom, "type": "joueur", "action": "delete"}
        try:
            requests.post("http://127.0.0.1:8080/webhook-endpoint/", json=payload)
            print(f"🚨 Suppression envoyée pour le joueur {instance.nom}")
        except requests.RequestException as e:
            print("Erreur webhook (delete joueur):", e)

    transaction.on_commit(send_webhook)


@receiver(post_save, sender=Entraineur)
def notify_webhook_receiver_Entraineur(sender, instance, created, **kwargs):
    def send_webhook():

        payload = {"id": instance.id_En, "nom": instance.nom, "type": "entraineur", "action": "update"}
        try:
            requests.post("http://127.0.0.1:8080/webhook-endpoint/", json=payload)
            print(f"🚨 Post envoyée pour l'entraineur {instance.nom}")
        except requests.RequestException as e:
            print("Erreur webhook :", e)

    transaction.on_commit(send_webhook)


@receiver(post_delete, sender=Entraineur)
def notify_webhook_delete_entraineur(sender, instance, **kwargs):
    def send_webhook():

        payload = {"id": instance.id_En, "nom": instance.nom, "type": "entraineur", "action": "delete"}
        try:
            requests.post("http://127.0.0.1:8080/webhook-endpoint/", json=payload)
            print(f"🚨 Suppression envoyée pour l'entraineur {instance.nom}")
        except requests.RequestException as e:
            print("Erreur webhook (delete entraineur):", e)

    transaction.on_commit(send_webhook)


@receiver(m2m_changed, sender=Equipe.joueurs.through)
def notify_webhook_receiver_Equipe(sender, instance, action, **kwargs):

    def send_webhook():

        payload = {"id": instance.id_Eq, "nom": instance.nom, "type": "equipe", "action": "update"}
        try:
            requests.post("http://127.0.0.1:8080/webhook-endpoint/", json=payload)
            print(f"🚨 Post envoyée pour l'équipe {instance.nom}")
        except requests.RequestException as e:
            print("Erreur webhook :", e)

    if action == "post_add":
        transaction.on_commit(send_webhook)


@receiver(post_delete, sender=Equipe)
def notify_webhook_delete_equipe(sender, instance, **kwargs):

    def send_webhook():

        payload = {"id": instance.id_Eq, "nom": instance.nom, "type": "equipe", "action": "delete"}
        try:
            requests.post("http://127.0.0.1:8080/webhook-endpoint/", json=payload)
            print(f"🚨 Suppression envoyée pour l'équipe {instance.nom}")
        except requests.RequestException as e:
            print("Erreur webhook (delete équipe):", e)

    transaction.on_commit(send_webhook)
