from django import forms
from .models import *
from django.forms.formsets import BaseFormSet
from django.forms.models import inlineformset_factory, formset_factory, modelformset_factory
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.contrib.admin.widgets import AdminDateWidget


class LoginForm(forms.Form):
    nom_d_utilisateur = forms.CharField()
    mot_de_passe = forms.CharField(widget=forms.PasswordInput)

class changepwd(forms.Form):
    Ancien_mot_de_passe = forms.CharField()
    Nouveau_mot_de_passe = forms.CharField(widget=forms.PasswordInput)
    Confirmer_nouveau_mot_de_passe = forms.CharField(widget=forms.PasswordInput)

class EmployeAjoutForm(forms.ModelForm):
    class Meta:
        model = Employe
        exclude = ['actif',]


class employe_consult(forms.ModelForm):
    class Meta:
        model = Employe
        fields = ['user',]


class EmployeUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True, label='Nom et prénom')
    email = forms.EmailField(max_length=254, required=True, label='Email')
    GRADE_CHOICES = Employe.grade[:6]
    fonction = forms.ChoiceField(choices=GRADE_CHOICES, label='Fonction')
    class Meta:
        model = Employe
        fields = [
            # "user__first_name",
            "fonction",
            # "user__email",
            "phone",

            
        ]

    solde_conge = forms.DecimalField(required=False)
    solde_conge_maladie = forms.DecimalField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate solde_conge field with the current value

        if self.instance and self.instance.nbrEmp.exists():
            self.fields['solde_conge'].initial = self.instance.nbrEmp.last().solde_conge
            self.fields['solde_conge_maladie'].initial = self.instance.nbrEmp.last().solde_conge_maladie
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['email'].initial = self.instance.user.email
class EmployeDesactivateForm(forms.ModelForm):
    class Meta:
        model = Employe
        fields = [
            "actif", 
                    ]

class UserRegistrationForm(forms.ModelForm):

  
    phone = forms.CharField(validators=[RegexValidator(regex=r'^\d{8}$', message="Entrer un numéro de 8 chiffres")], required=True)
    password = forms.CharField(label='Password',widget=forms.PasswordInput)
    password2 = forms.CharField(label='Resaisir password',widget=forms.PasswordInput)
    
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']
        labels = {
            'first_name': 'Nom & prénom',

        }
    # def clean_password2(self):
    #     cd = self.cleaned_data
    #     if cd['password'] != cd['password2']:
    #         raise forms.ValidationError('Les mots de passe ne sont pas identiques.')
    #     return cd['password2']
    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['first_name'].required = True
        self.fields['email'].required = True
     
        for fieldname in ['username',]:
            self.fields[fieldname].help_text = None

 
   
 
class ddecongeForm(forms.ModelForm):
    
    class Meta:
        model = PasserConge
        exclude = [
            "employee", "Accepte" ,"Refuse"
                    ]
        widgets={
            'DateDebut': forms.DateInput(
                format=('%d/%m/%Y'),
                
                attrs={'class': 'form-control', 
                        
                       'type': 'date'  # <--- IF I REMOVE THIS LINE, THE INITIAL VALUE IS DISPLAYED
                      }
                      
                      ),
            'duree':forms.TextInput(
                attrs={"id":"id_duree"}),
            'DateFin': forms.DateInput(
                format=('%d/%m/%Y'),
                attrs={'class': 'form-control', 
                        'readonly' : 'readonly',
                       'type': 'date'  # <--- IF I REMOVE THIS LINE, THE INITIAL VALUE IS DISPLAYED
                      }),
                      

            }
        labels = {
            'DateDebut': 'Date Début du congé',
            'DateFin': 'Date Fin du congé',
            'duree': 'Durée du congé',
        }
        
    def __init__(self, *args, **kwargs):
    
        super().__init__(*args, **kwargs)
        self.fields['DateDebut'].widget.attrs['onchange'] = 'update_duration()'
        self.fields['duree'].widget.attrs['onchange'] = 'update_duration()'
        
        # self.fields['duree'].readonly = True

