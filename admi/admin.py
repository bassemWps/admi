from django.contrib import admin

from .models import *
# Register your models here.
@admin.register(Employe)
class EmployeAdmin(admin.ModelAdmin):
    list_display = ['user', 'fonction','date_embauche','phone']
    list_filter = ['user', 'fonction','date_embauche','phone']
    search_fields = ['user', 'fonction','date_embauche','phone']
    ordering = ['user']
    def user_email(self, obj):
        return Employe.user.email



@admin.register(Compte)
class compteAdmin(admin.ModelAdmin):
    list_display = ['annee', 'employee',"solde_conge","solde_conge_maladie"]
    list_filter = ['annee', 'employee',"solde_conge","solde_conge_maladie"]
    search_fields = ['annee', 'employee',"solde_conge","solde_conge_maladie"]
    ordering = ['annee','employee']

@admin.register(PasserConge)
class PasserCongeAdmin(admin.ModelAdmin):
    list_display = ['employee', 'DateDemande', 'DateDebut',"DateFin","Accepte","Refuse"]
    list_filter = ['employee', 'DateDemande','DateDebut',"DateFin","Accepte","Refuse"]
    search_fields = ['employee', 'DateDemande','DateDebut',"DateFin","Accepte","Refuse"]
    ordering = ['employee','Accepte']


