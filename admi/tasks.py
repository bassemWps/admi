# from celery import shared_task
# from django.core.mail import send_mail
# from django.conf import settings
# from django.shortcuts import render, get_object_or_404,redirect
# from .models import *
# @shared_task
# def increment_solde_conge():
#     # Logique pour incrémenter le champ solde_conge du modèle Compte
#     # Par exemple, en ajoutant 1 à solde_conge à la fin de chaque mois
#     comptes = Compte.objects.all()
#     for compte in comptes:
#         compte.solde_conge += 1.5
#         compte.solde_conge_maladie += 1.5
#         compte.save()

# @shared_task
# def raz_solde():
#     # Logique pour incrémenter le champ solde_conge du modèle Compte
#     # Par exemple, en ajoutant 1 à solde_conge à la fin de chaque mois
#     comptes = Compte.objects.all()
#     for compte in comptes:
#         Compte.objects.create(annee=current_year(),employee = compte.employee,solde_conge=0,solde_conge_maladie =0)
