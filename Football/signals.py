# ton_app/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Joueur, Entraineur, Equipe
import requests

@receiver(post_save, sender=Joueur)
def notify_webhook_receiver_Joueur(sender, instance, created, **kwargs):
    payload = {
        "id" : instance.id_J,
        "nom" : instance.nom,
    }
    try:
        requests.post("http://projet-b.local/webhook-endpoint/Joueur/", json=payload)
    except requests.RequestException as e:
        print("Erreur webhook :", e)


@receiver(post_save, sender=Entraineur)
def notify_webhook_receiver_Entraineur(sender, instance, created, **kwargs):
    payload = {
        "id" : instance.id_En,
        "nom" : instance.nom,
    }
    try:
        requests.post("http://projet-b.local/webhook-endpoint/Entraineur/", json=payload)
    except requests.RequestException as e:
        print("Erreur webhook :", e)


@receiver(post_save, sender=Equipe)
def notify_webhook_receiver_Equipe(sender, instance, created, **kwargs):
    payload = {
        "id" : instance.id,
        "nom" : instance.nom,
    }
    try:
        requests.post("http://projet-b.local/webhook-endpoint/Equipe/", json=payload)
    except requests.RequestException as e:
        print("Erreur webhook :", e)
