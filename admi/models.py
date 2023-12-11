from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from decimal import *
import datetime
from django.conf import settings

from django.core.validators import RegexValidator



def current_year():
    return datetime.date.today().year


def max_value_current_year(value):
    ab = current_year() + 50 
    return MaxValueValidator(ab)(value)


class Employe(models.Model):

    grade = (
  ('Superviseur', 'Superviseur'),
  ('Comptable', 'Comptable'),
  ('Administratif', 'Administratif'),
  ('Delegué', 'Delegué'),
  ('Livreur', 'Livreur'),
  ('Coursier', 'Coursier'),
  ('Administrateur', 'Administrateur'),
  
 )
    phone_regex = RegexValidator(
    regex=r'^\d{8}$',
    message="Entrer un numéro de 8 chiffres",
)
    user = models.OneToOneField(settings.AUTH_USER_MODEL,related_name='uzer',on_delete=models.CASCADE)   
    #nom_employe = models.CharField(max_length=200,unique = True)
    #slug = models.SlugField(max_length=200)
    phone = models.CharField(validators=[phone_regex], max_length=8,
                             null=True, blank=True)
    fonction = models.CharField(max_length=50, choices=grade, default='Delegué')
    #email = models.EmailField()
    date_embauche = models.DateField(auto_now_add=True)
    actif = models.BooleanField(default=True)


    class Meta:
        ordering = ['user']
        indexes = [

models.Index(fields=['user']),

]
    def __str__(self):
        return self.user.first_name
    def get_absolute_url(self):
        return reverse('admi:employe_detail', args=[self.id])
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.nbrEmp.exists():
            Compte.objects.create(annee=current_year(), employee=self,solde_conge =0,solde_conge_maladie =0)

        

class Compte(models.Model):
    annee = models.PositiveIntegerField(default=current_year(), 
            validators=[MinValueValidator(2015), max_value_current_year])
    employee = models.ForeignKey(Employe,on_delete=models.CASCADE,related_name='nbrEmp', blank=True,null=True)
    solde_conge = models.DecimalField( decimal_places=2,default=0, validators=[MinValueValidator(Decimal('0'))], max_digits=12)
    solde_conge_maladie = models.DecimalField( decimal_places=2,default=0, validators=[MinValueValidator(Decimal('0'))], max_digits=12)
    def __str__(self):
        return f"{self.employee.user.first_name} année {self.annee}"
    class Meta:
        ordering = ['annee']

class PasserConge(models.Model):
    type_conge = (
  ('Congé de Maladie', 'Congé de Maladie'),
  ('Congé Annuel', 'Congé Annuel'),
  
  
 )
    employee = models.ForeignKey(Employe,on_delete=models.CASCADE,related_name='CongEmp', blank=True,null=True)
    type_conge= models.CharField(max_length=50, choices=type_conge, default='Congé Annuel')
    DateDemande=models.DateField(auto_now_add=True)
    DateDebut = models.DateField()
    duree = models.DecimalField( decimal_places=2, validators=[MinValueValidator(Decimal('0'))], max_digits=12)

    DateFin = models.DateField()
    Accepte = models.BooleanField(default=False)
    Refuse = models.BooleanField(default=False)

