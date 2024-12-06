# Sustainable_platform/settings.py

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Add the required middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware', 
    'django.contrib.auth.middleware.AuthenticationMiddleware',  
    'django.contrib.messages.middleware.MessageMiddleware', 
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # Ensure this comes before AuthenticationMiddleware
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# TEMPLATES setting
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'recommendations/templates/recommendations',
        ],
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

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

DEBUG = True
ROOT_URLCONF = 'Sustainable_platform.urls'

# Installed apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'recommendations',

]


SECRET_KEY = '1234'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Using SQLite as the database engine
        'NAME': BASE_DIR / 'db.sqlite3',  # Path to the SQLite database file
    }
}

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# AUTH_USER_MODEL = 'recommendations.CustomUser'