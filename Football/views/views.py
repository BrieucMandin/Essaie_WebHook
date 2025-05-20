from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt  # Important pour permettre au webhook de POST sans CSRF token
def webhook_receiver(request):
    if request.method == "POST":
        payload = json.loads(request.body)

        # Ici tu peux traiter ton payload
        print("Webhook reçu :", payload)

        return JsonResponse({"status": "success"})
    else:
        return JsonResponse({"error": "Méthode non autorisée"}, status=405)
