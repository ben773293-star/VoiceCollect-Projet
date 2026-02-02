import os
from pathlib import Path
import dj_database_url

# Chemin de base du projet
BASE_DIR = Path(__file__).resolve().parent.parent

# SÉCURITÉ : Garde cette clé secrète en production !
SECRET_KEY = 'django-insecure-v-ta-cle-specifique-ici-ne-pas-partager'

# SÉCURITÉ : True en développement, False en production
DEBUG = True

ALLOWED_HOSTS = ['*']

# Définition des Applications
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'reports', # Ton application de suivi-évaluation
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# Base de données
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Validation des mots de passe
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# Internationalisation (Configuré pour le Burkina Faso)
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Ouagadougou'
USE_I18N = True
USE_TZ = True

# Fichiers Statiques (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# --- CONFIGURATION DES FICHIERS MÉDIAS (AUDIOS) ---
# On ajoute 'cloudinary_storage' et 'cloudinary' AVANT 'django.contrib.staticfiles'
INSTALLED_APPS = [
    'django.contrib.admin',           # <-- Vérifie bien celle-ci
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary_storage',
    'cloudinary',
    'app_voice',                      # Le nom de ton dossier d'application
]

# Configuration de Cloudinary
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'TON_CLOUD_NAME',
    'API_KEY': 'TON_API_KEY',
    'API_SECRET': 'TON_API_SECRET'
}

# On change le moteur de stockage par défaut
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.RawMediaCloudinaryStorage'

# --- CONFIGURATION IA WHISPER ---
# Remplace par ta vraie clé API OpenAI
OPENAI_API_KEY = "sk-votre-cle-ici"

# Redirection après connexion/déconnexion
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Si on est sur Render, on utilise leur base de données, sinon on reste en local (SQLite)
DATABASES = {
    'default': dj_database_url.config(
        # Cette ligne permet d'utiliser SQLite en local et PostgreSQL sur Render
        default=os.environ.get('DATABASE_URL', 'sqlite:///db.sqlite3'),
        conn_max_age=600
    )
}
    # Dans core/settings.py
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'dyfjvrwjr',
    'API_KEY': '971547724522531',
    'API_SECRET': 'hiVwykP2rn... (ta clé complète)',
} # <--- Assure-toi qu'il n'y a RIEN après cette accolade