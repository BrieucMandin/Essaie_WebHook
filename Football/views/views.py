from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt  # Important pour permettre au webhook de POST sans CSRF token
def webhook_receiver(request):
    """
    Réceptionne et traite les requêtes POST d'un webhook externe.

    Cette vue accepte uniquement les requêtes HTTP de type POST. Elle désérialise
    le contenu JSON du corps de la requête, l'affiche dans la console pour traitement,
    puis renvoie une réponse JSON de confirmation.

    La protection CSRF est désactivée via le décorateur ``@csrf_exempt`` pour permettre
    la réception de requêtes provenant de sources externes non authentifiées.

    :param request: Objet HttpRequest contenant les données de la requête.
    :type request: HttpRequest

    :return: Réponse JSON indiquant le succès ou une erreur 405 si la méthode n'est pas POST.
    :rtype: JsonResponse

    :Example:

    .. code-block:: http-request

        POST /webhook-endpoint/
        Content-Type: application/json

        {
            "id": 1,
            "nom": "John Doe",
            "type": "joueur",
            "action": "update"
        }

    :status 200: Requête POST traitée avec succès.
    :status 405: Méthode HTTP non autorisée (autre que POST).
    """

    if request.method == "POST":
        payload = json.loads(request.body)

        # Ici tu peux traiter ton payload
        print("Webhook reçu :", payload)

        return JsonResponse({"status": "success"})
    else:
        return JsonResponse({"error": "Méthode non autorisée"}, status=405)
