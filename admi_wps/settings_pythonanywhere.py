from .settings import *

# Ajoutez ou remplacez les paramètres spécifiques à PythonAnywhere
# DEBUG = False

ALLOWED_HOSTS = ['bassemadmi.pythonanywhere.com']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bassemAdmi$admi',
        'USER': 'bassemAdmi',
        'PASSWORD': 'bassem79',
        'HOST': 'bassemAdmi.mysql.pythonanywhere-services.com',
        'PORT': '3306',
    }
}