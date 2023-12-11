
from celery import shared_task
from django.utils import timezone
from .models import Compte

@shared_task
def update_solde_conge():
    # Logique pour incrémenter le champ solde_conge du modèle Compte
    # Par exemple, en ajoutant 1 à solde_conge à la fin de chaque mois
    comptes = Compte.objects.all()
    current_month = timezone.now().month
    current_day = timezone.now().day
    if current_day == 1:
        for compte in comptes:
            compte.solde_conge += 1.5
            compte.solde_conge_maladie += 1.5
            compte.save()

    # Logique pour réinitialiser le champ solde_conge à la fin de chaque année
    if current_month == 1 and current_day == 1:
        for compte in comptes:
            Compte.objects.create(
                annee=timezone.now().year,
                employee=compte.employee,
                solde_conge=0,
                solde_conge_maladie=0
            )