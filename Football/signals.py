# ton_app/signals.py
import requests
import time

from django.db.models.signals import post_delete, post_save, m2m_changed
from django.db import transaction
from django.dispatch import receiver

from .models import Joueur, Entraineur, Equipe


@receiver(post_save, sender=Joueur)
def notify_webhook_receiver_Joueur(sender, instance, created, **kwargs):
    """
    Envoie une requête POST à un endpoint webhook après la sauvegarde (création ou mise à jour) d'une instance de Joueur.

    :param sender: Le modèle qui a envoyé le signal (ici, `Joueur`).
    :type sender: Model
    :param instance: L'instance de `Joueur` qui a été sauvegardée.
    :type instance: Joueur
    :param created: Indique si l'instance a été créée (`True`) ou mise à jour (`False`).
    :type created: bool
    :param kwargs: Paramètres supplémentaires du signal.
    :type kwargs: dict

    :note: Le webhook est envoyé uniquement après la validation de la transaction (`transaction.on_commit`).
    """

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
    """
    Envoie une requête POST à un endpoint webhook après la suppression d'une instance de Joueur.

    :param sender: Le modèle qui a envoyé le signal (ici, `Joueur`).
    :type sender: Model
    :param instance: L'instance de `Joueur` qui a été supprimée.
    :type instance: Joueur
    :param kwargs: Paramètres supplémentaires du signal.
    :type kwargs: dict

    :note: Le webhook est envoyé uniquement après la validation de la transaction (`transaction.on_commit`).
    """

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
    """
    Envoie une requête POST à un endpoint webhook après la sauvegarde (création ou mise à jour) d'une instance d'Entraineur.

    :param sender: Le modèle qui a envoyé le signal (ici, `Entraineur`).
    :type sender: Model
    :param instance: L'instance de `Entraineur` qui a été sauvegardée.
    :type instance: Entraineur
    :param created: Indique si l'instance a été créée (`True`) ou mise à jour (`False`).
    :type created: bool
    :param kwargs: Paramètres supplémentaires du signal.
    :type kwargs: dict

    :note: Le webhook est envoyé uniquement après la validation de la transaction (`transaction.on_commit`).
    """

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
    """
    Envoie une requête POST à un endpoint webhook après la suppression d'une instance d'Entraineur.

    :param sender: Le modèle qui a envoyé le signal (ici, `Entraineur`).
    :type sender: Model
    :param instance: L'instance de `Entraineur` qui a été supprimée.
    :type instance: Entraineur
    :param kwargs: Paramètres supplémentaires du signal.
    :type kwargs: dict

    :note: Le webhook est envoyé uniquement après la validation de la transaction (`transaction.on_commit`).
    """

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
    """
    Envoie une requête POST à un endpoint webhook après qu'un ou plusieurs joueurs ont été ajoutés à une équipe.

    :param sender: Le modèle intermédiaire de la relation many-to-many (`Equipe.joueurs.through`).
    :type sender: Model
    :param instance: L'instance de `Equipe` concernée par la modification.
    :type instance: Equipe
    :param action: L'action m2m déclenchée (par exemple : 'post_add').
    :type action: str
    :param kwargs: Paramètres supplémentaires du signal.
    :type kwargs: dict

    :note: Le webhook est déclenché uniquement après l'ajout effectif de joueurs (`action == "post_add"`) et après validation de la transaction (`transaction.on_commit`).
    """

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
    """
    Envoie une requête POST à un endpoint webhook après la suppression d'une instance d'Equipe.

    :param sender: Le modèle qui a envoyé le signal (ici, `Equipe`).
    :type sender: Model
    :param instance: L'instance de `Equipe` qui a été supprimée.
    :type instance: Equipe
    :param kwargs: Paramètres supplémentaires du signal.
    :type kwargs: dict

    :note: Le webhook est envoyé uniquement après la validation de la transaction (`transaction.on_commit`).
    """

    def send_webhook():

        payload = {"id": instance.id_Eq, "nom": instance.nom, "type": "equipe", "action": "delete"}
        try:
            requests.post("http://127.0.0.1:8080/webhook-endpoint/", json=payload)
            print(f"🚨 Suppression envoyée pour l'équipe {instance.nom}")
        except requests.RequestException as e:
            print("Erreur webhook (delete équipe):", e)

    transaction.on_commit(send_webhook)
