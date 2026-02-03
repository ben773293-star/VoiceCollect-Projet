#!/usr/bin/env bash
# Arrêter le script en cas d'erreur
set -o errexit

# Installer les dépendances
pip install -r requirements.txt

# Appliquer les migrations (préparer la base de données)
python manage.py migrate
python manage.py createsuperuser --noinput --username Rachid226 --email ben773293@gmail.com || true
