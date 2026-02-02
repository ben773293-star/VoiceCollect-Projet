#!/usr/bin/env bash
# Arrêter le script en cas d'erreur
set -o errexit

# Installer les dépendances
pip install -r requirements.txt

# Appliquer les migrations (préparer la base de données)
python manage.py migrate