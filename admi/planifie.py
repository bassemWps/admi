import sys
from pathlib import Path
import os
import django

# Ajoutez le chemin du répertoire parent du projet au sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

# Définissez DJANGO_SETTINGS_MODULE pour indiquer où trouver les paramètres Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'admi_wps.settings_pythonanywhere'  # Chemin relatif à BASE_DIR


# Initialisation de l'environnement Django
django.setup()

# Importez maintenant les modules Django
from django.utils import timezone
from admi.apps import AdmiConfig  # Modifiez cette ligne pour importer votre AppConfig
from admi.models import Compte,Employe
from decimal import Decimal


import schedule
import time

def update_solde_conge():
    # Logique pour incrémenter le champ solde_conge du modèle Compte
    # Par exemple, en ajoutant 1 à solde_conge à la fin de chaque mois
    comptes = Compte.objects.filter(annee=timezone.now().year)
    employee = Employe.objects.filter(actif=True)
    current_month = timezone.now().month
    current_day = timezone.now().day
    if current_day == 1 and current_month != 1:
        for compte in comptes:
            compte.solde_conge += Decimal('1.5')
            compte.solde_conge_maladie += Decimal('1.25')
            compte.save()

    # Logique pour réinitialiser le champ solde_conge à la fin de chaque année
    if current_month == 1 and current_day == 1 :
        for em in employee:
            Compte.objects.create(
                annee=timezone.now().year,
                employee=em,
                solde_conge=Decimal('0'),
                solde_conge_maladie=Decimal('0')
            )

# # schedule.every(1).minutes.do(update_solde_conge) 
# schedule.every().day.at('00:00').do(update_solde_conge)

# # Boucle pour exécuter la planification en continu
# while True:
#     schedule.run_pending()
#     time.sleep(1)  # Attendre 1 seconde entre les vérifications

update_solde_conge()