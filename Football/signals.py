# ton_app/signals.py
import requests

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Joueur, Entraineur, Equipe


@receiver(post_save, sender=Joueur)
def notify_webhook_receiver_Joueur(sender, instance, created, **kwargs):
    payload = {
        "id" : instance.id_J,
        "nom" : instance.nom,
        "type": "Joueur",
    }
    try:
        requests.post("http://127.0.0.1:8080/webhook-endpoint/", json=payload)
        print(f"🚨 Post envoyée pour le joueur {instance.nom}")
    except requests.RequestException as e:
        print("Erreur webhook :", e)


@receiver(post_delete, sender=Joueur)
def notify_webhook_delete_Joueur(sender, instance, **kwargs):
    payload = {
        "id": instance.id_J,
        "nom": instance.nom,
        "type": "joueur",
        "action": "delete"
    }
    try:
        requests.post("http://127.0.0.1:8080/webhook-endpoint/", json=payload)
        print(f"🚨 Suppression envoyée pour le joueur {instance.nom}")
    except requests.RequestException as e:
        print("Erreur webhook (delete joueur):", e)


@receiver(post_save, sender=Entraineur)
def notify_webhook_receiver_Entraineur(sender, instance, created, **kwargs):
    payload = {
        "id" : instance.id_En,
        "nom" : instance.nom,
        "type": "entraineur",
    }
    try:
        requests.post("http://127.0.0.1:8080/webhook-endpoint/", json=payload)
        print(f"🚨 Post envoyée pour l'entraineur {instance.nom}")
    except requests.RequestException as e:
        print("Erreur webhook :", e)


@receiver(post_delete, sender=Entraineur)
def notify_webhook_delete_entraineur(sender, instance, **kwargs):
    payload = {
        "id": instance.id_En,
        "nom": instance.nom,
        "type": "entraineur",
        "action": "delete"
    }
    try:
        requests.post("http://127.0.0.1:8080/webhook-endpoint/", json=payload)
        print(f"🚨 Suppression envoyée pour l'entraineur {instance.nom}")
    except requests.RequestException as e:
        print("Erreur webhook (delete entraineur):", e)


@receiver(post_save, sender=Equipe)
def notify_webhook_receiver_Equipe(sender, instance, created, **kwargs):
    payload = {
        "id" : instance.id,
        "nom" : instance.nom,
        "type": "equipe",
    }
    try:
        requests.post("http://127.0.0.1:8080/webhook-endpoint/", json=payload)
        print(f"🚨 Post envoyée pour l'équipe {instance.nom}")
    except requests.RequestException as e:
        print("Erreur webhook :", e)


@receiver(post_delete, sender=Equipe)
def notify_webhook_delete_equipe(sender, instance, **kwargs):
    payload = {
        "id": instance.id,
        "nom": instance.nom,
        "type": "equipe",
        "action": "delete"
    }
    try:
        requests.post("http://127.0.0.1:8080/webhook-endpoint/", json=payload)
        print(f"🚨 Suppression envoyée pour l'équipe {instance.nom}")
    except requests.RequestException as e:
        print("Erreur webhook (delete équipe):", e)
