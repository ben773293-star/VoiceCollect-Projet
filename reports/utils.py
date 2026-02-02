import openai
import os
from django.conf import settings

def transcribe_audio(file_path):
    """
    Fonction experte pour transformer un fichier audio en texte via Whisper.
    Prend en entrée le chemin complet du fichier (.mp3, .wav, .m4a, etc.)
    """
    
    # 1. Configuration de la clé API
    # Bonne pratique : On récupère la clé depuis les réglages Django
    openai.api_key = getattr(settings, "OPENAI_API_KEY", "TA_CLE_ICI")

    try:
        # 2. Ouverture du fichier binaire
        with open(file_path, "rb") as audio_file:
            # 3. Appel à l'API Whisper d'OpenAI
            # On utilise le modèle 'whisper-1' qui est le plus performant
            response = openai.Audio.transcribe(
                model="whisper-1", 
                file=audio_file
            )
            
            # 4. Retourne uniquement le texte transcrit
            return response.get('text', '')

    except Exception as e:
        # En cas d'erreur (réseau, clé invalide), on enregistre l'erreur dans la console
        print(f"Erreur lors de la transcription IA : {str(e)}")
        # On retourne un message explicatif pour ne pas bloquer l'application
        return "[Erreur de transcription : L'IA n'a pas pu traiter ce fichier]"

def get_audio_duration(file_path):
    """
    Fonction bonus : Utile pour les statistiques MEAL
    Permet de connaître la durée du rapport vocal (nécessite pydub ou similaire)
    """
    # Pour l'instant, nous restons sur la transcription simple
    pass