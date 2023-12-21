from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.db.models import Count,Q,Sum,F,ExpressionWrapper,Case, Value, When,Max,Subquery,OuterRef,FloatField
from .models import *
from .forms import *
from django.urls import reverse_lazy,reverse
from django.shortcuts import render, get_object_or_404,redirect
from django.views.generic import CreateView,UpdateView,DeleteView
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib import messages
from django.conf import settings
import os
from django.http import JsonResponse
from django.views.generic.edit import FormView
from datetime import date,datetime
from django.db.models.functions import (
    ExtractDay, ExtractMonth, ExtractQuarter, ExtractWeek,
     ExtractIsoWeekDay, ExtractWeekDay, ExtractIsoYear, ExtractYear,
 )
from django.db.models import Count
from django.db import IntegrityError, transaction
from django.db.models.functions import Cast
from django.db.models import IntegerField,DecimalField,CharField
from django.contrib.auth import authenticate, login, logout
from datetime import timedelta,date
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.db.models import ProtectedError
from django.core.mail import send_mail


def dashboard(request):
    #seuil = Produit.objects.filter(quantite_stock__lte = F('seuil'))
    query = request.GET.get('q')
    request.session['recherche'] = query
    if query:
        emp=Employe.objects.filter(
            Q(user__first_name__icontains=query)).exclude(fonction='Administrateur'

            ).distinct()

        cg=PasserConge.objects.filter(
            employee__user__first_name__icontains=query).exclude(employee__fonction='Administrateur'
            
            ).distinct()



    return render(request, 'dashboard.html', locals())

def user_login(request):
    next = request.POST.get('next', request.GET.get('next', ''))

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['nom_d_utilisateur'], password=cd['mot_de_passe'])
            if user is not None:

                login(request, user)
                request.session['utilisateur'] = cd['nom_d_utilisateur']
                request.session['mot_de_passe'] = cd['mot_de_passe']
                msg = "Vous êtes maintenant connecté."


                

                messages.success(request, msg)
                if next:
                    return HttpResponseRedirect(next)

            else:
                messages.warning(request, "Vérifier vos paramètres de connexion.")
            return redirect('admi:dashboard')
    else:
        form = LoginForm()
        ctx = {'form': form, 'next': next}
    return render(request, 'connexion.html', locals())


@login_required
def deconnexion(request):
    logout(request)
    messages.success(request, f'Vous avez été deconnecté')
    return redirect('admi:connexion')

import re
def register(request):
    if request.method == 'POST':
        if User.objects.filter(email=request.POST.get('email')).exists():  
            messages.warning(request,"Veuillez choisir un autre email utilisateur")
            return redirect('admi:connexion')
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
            user_form.cleaned_data['password'])
           
            new_user.save()
            Employe.objects.create(user=new_user,phone=user_form.cleaned_data['phone'],actif=True)
        else:
            phone_regex = re.compile(r'^\d{8}$')
            if request.POST.get('password') != request.POST.get('password2'):
                messages.warning(request,"Les mots de passe ne sont pas identiques")
                print(f"{request.POST.get('password')} et  {request.POST.get('password2')}")
            if not phone_regex.match(request.POST.get('phone')):
                messages.warning(request,"Un numéro de tel doit comporter 8 chiffres")
            if User.objects.filter(username=request.POST.get('username')).exists(): 
                messages.warning(request,"Veuillez choisir un autre nom utilisateur")


            
            messages.warning(request,"Un problème est survenu")
            return redirect('admi:connexion')
        messages.success(request, f'Votre compte à été créée avec succés')
        return redirect('admi:connexion')

    else:
        user_form = UserRegistrationForm()
    return render(request,'register.html',{'user_form':user_form})

@login_required(redirect_field_name=None)
def changepassword(request):
    if request.method == 'POST':
        form = changepwd(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['Ancien_mot_de_passe'] != request.session['mot_de_passe']:
                messages.warning(request, "Vérifier votre ancien mot de passe.")
                return redirect('admi:deconnexion')
            else:
                if cd['Nouveau_mot_de_passe'] != cd['Confirmer_nouveau_mot_de_passe']:
                    messages.warning(request, "Les mots de passe ne correspondent pas. Opération avortée")
                    return redirect(reverse('admi:changepassword'))
                else:
                    user = request.user
                    user.set_password(form.cleaned_data['Nouveau_mot_de_passe'])
                    user.save()
                    update_session_auth_hash(request, user)
                    messages.success(request, "mot de passe changé.")
                    return redirect(reverse('admi:connexion'))
    else:
        form = changepwd()
    return render(request, 'change_password.html', {'form': form})


@method_decorator(staff_member_required, name='dispatch')
class employe_ajouter(CreateView):
    model = Employe
    form_class = EmployeAjoutForm
    template_name = "Employe_ajouter.html"
    def get_success_url(self):
        messages.success(self.request,f'Employé ajouté avec succés')
        return (reverse('admi:employe_list'))

@method_decorator(staff_member_required, name='dispatch')
class employe_supprimer(DeleteView):
    model = Employe
  
    template_name = "employe_supprimer.html"
    def get_success_url(self):
        messages.success(self.request,f'Employé supprimé avec succés')
        return (reverse('admi:employe_list'))



@method_decorator(login_required, name='dispatch')    
class EmployeUpdateView(UpdateView):
    model = Employe
    form_class = EmployeUpdateForm
    template_name = "employe_modifier.html"
    context_object_name = "emp"

    def get_success_url(self):
        messages.success(self.request,f'Employé mis à jour avec succés')
        return (reverse('admi:employe_list'))
    def form_valid(self, form):
        # Handle form validation and save logic here
        if form.is_valid():
            employe = form.save(commit=False)
            
            # Access the new value of solde_conge from the form's cleaned data
            new_solde_conge = form.cleaned_data['solde_conge']
            new_solde_conge_maladie = form.cleaned_data['solde_conge_maladie']
            new_nom =form.cleaned_data['first_name']
            new_email= form.cleaned_data['email']

            
              
            employe.user.first_name=new_nom
            employe.user.email =new_email
                
            if employe.nbrEmp.exists():
                compte_instance = employe.nbrEmp.last()
                compte_instance.solde_conge = new_solde_conge
                compte_instance.solde_conge_maladie = new_solde_conge_maladie
                compte_instance.save()

            employe.user.save()   
            employe.save()
            # Vérifier si le formulaire provient du formset
            if form.is_bound:
                messages.success(self.request, 'Employé mis à jour avec succès')
                
                return HttpResponseRedirect(self.get_success_url())

           
            
        return super().form_valid(form)



@method_decorator(staff_member_required, name='dispatch')
class EmployeDesactivateView(UpdateView):
    model = Employe
    form_class = EmployeDesactivateForm
    template_name = "employe_modifier.html"
    context_object_name = "emp"


    def get_success_url(self):
        messages.success(self.request,f'Employé désactivé avec succés')
        return (reverse('admi:employe_list'))


@staff_member_required
def employe_list(request):

    annee_en_cours = ExtractYear(date.today())
    employe = Employe.objects.filter(actif=True).exclude(fonction='Administrateur')

    employes_avec_nombre_conges = employe.annotate(
        nombre_conges_annuels=Sum(
            Case(
                When(CongEmp__DateDebut__year=annee_en_cours, CongEmp__Accepte=True, CongEmp__type_conge='Congé Annuel',  then=F('CongEmp__duree')),default=0,
                output_field=DecimalField()
            )
        ),
        nombre_conges_maladie=Sum(
            Case(
                When(CongEmp__DateDebut__year=annee_en_cours, CongEmp__Accepte=True, CongEmp__type_conge='Congé de Maladie',  then=F('CongEmp__duree')),default=0,
                output_field=DecimalField()
            )
        ),
    )


    return render(request, 'employe_list.html', {'emp'  : employes_avec_nombre_conges ,
                                               
                                                } )


@staff_member_required
def employe_list2(request,pk=None):

    
    employe = Employe.objects.filter(actif=True).exclude(fonction='Administrateur')

    if request.session.get('recherche', None): 
       employe=employe.filter(pk=pk)
      

    return render(request, 'employe_list.html', {'emp'  : employe ,
                                               
                                                } )
@login_required
def demander_conge(request,pk):
    annee_en_cours = ExtractYear(date.today())
    if request.method == 'POST':
        form = ddecongeForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data 


            try :
                krap = Compte.objects.get(employee=request.user.uzer, annee=ExtractYear(cd["DateDebut"]))
                km = krap.solde_conge_maladie
                kc = krap.solde_conge
                
            except:
                
                km = 0
                kc = 0

            if ((cd ["type_conge"] == "Congé de Maladie" and cd["duree"] > km)
            or (cd ["type_conge"] == "Congé Annuel" and cd["duree"] > kc)):
                messages.warning(request,"Attention vous avez dépassé votre solde! Réduisez la durée de votre congé")
                return redirect('admi:employe_conge',request.user.uzer.id)
            elif cd["DateDebut"] < date.today():
                messages.warning(request,"Attention vérifier la date de début de votre congé")
                return redirect('admi:employe_conge',request.user.uzer.id)
            else:
                kong= form.save(commit=False)
                nouveau = PasserConge.objects.create(employee = request.user.uzer,
                type_conge= kong.type_conge,
                DateDebut = kong.DateDebut,
                DateFin= kong.DateFin,
                duree = kong.duree
                )



                desto= Employe.objects.filter(fonction="Administrateur").last()
                dest=desto.user.email
                subject = f"Demande de congé envoyé par {request.user.first_name}"
                message = f"Ceci est un message automatique. N'y répondez pas.\n On vous informe que l'employé {request.user.first_name} vous a envoyé une demande de congé de {kong.duree} jours à partir du "
                message += " {}" .format(kong.DateDebut.strftime("%d-%m-%Y \n"))
                url_absolue = request.build_absolute_uri(f'/employe/{nouveau.id}/traiter-demande_filtre')
                
                message += "Veuillez y répondre en suivant le lien suivant:\n"
                message += f"{url_absolue}"
            #message = message + usform.cleaned_data['rectification'].encode('utf8')

                send_mail(subject, message, settings.EMAIL_HOST_USER, [dest])
                sent = True






                messages.success(request,"Demande enregistré. Un mail à été envoyé au responsable pour validation")
                return redirect('admi:dashboard')

    else:
        form = ddecongeForm()
        
  
    return render(request, 'demande_conge.html', {'form': form, 'emp': request.user})




@login_required
def liste_demander_conge(request,pk,period=None):
    conge_accep = PasserConge.objects.filter(Accepte=True,employee=pk)
    conge_ref = PasserConge.objects.filter(Refuse=True,employee=pk)
    conge_att= PasserConge.objects.filter(Refuse=False,Accepte=False,employee=pk)
    yesterday = date.today() - timedelta(days=1)
    week = ExtractWeek(date.today())
    month= ExtractMonth(date.today())
    year = ExtractYear(date.today())
    
    if period == '1' :
        conge_accep = conge_accep.filter(DateDebut = date.today() )
        conge_ref = conge_ref.filter(DateDebut = date.today() )
        conge_att= conge_att.filter(DateDebut = date.today() )
    elif period == '2' :
        conge_accep = conge_accep.filter(DateDebut = yesterday )
        conge_ref = conge_ref.filter(DateDebut = yesterday )
        conge_att = conge_att.filter(DateDebut = yesterday )
    elif period == '3' :
        conge_accep = conge_accep.filter(DateDebut__week = week, DateDebut__month = month ,DateDebut__year = year )
        conge_ref = conge_ref.filter(DateDebut__week = week, DateDebut__month = month ,DateDebut__year = year )
        conge_att = conge_att.filter(DateDebut__week = week, DateDebut__month = month ,DateDebut__year = year )

    elif period == '4' :
        conge_accep = conge_accep.filter(DateDebut__month = month,DateDebut__year = year ) 
        conge_ref = conge_ref.filter(DateDebut__month = month,DateDebut__year = year ) 
        conge_att = conge_att.filter(DateDebut__month = month,DateDebut__year = year ) 
        
    elif period == '5' :
        conge_accep = conge_accep.filter(DateDebut__year = year )
        conge_ref = conge_ref.filter(DateDebut__year = year )
        conge_att = conge_att.filter(DateDebut__year = year )

    return render(request, 'conge_list.html', {'conge_accep':conge_accep,
                                               'conge_ref': conge_ref,
                                               'conge_att':conge_att,
                                               'cle' : pk,
                                                } )

@staff_member_required
def trait_demande_conge(request):
    date = datetime.now()
    dde = PasserConge.objects.filter(Refuse=False,Accepte=False,DateDebut__year=date.year)
    annee_en_cours = date.year
    dde = dde.annotate(
        nombre_conges_annuels=Sum(
            Case(
                When(employee__CongEmp__DateDebut__year=annee_en_cours, employee__CongEmp__Accepte=True, employee__CongEmp__type_conge='Congé Annuel',  then=F('employee__CongEmp__duree')),default=0,
                output_field=DecimalField()
            )
        ),
        nombre_conges_maladie=Sum(
            Case(
                When(employee__CongEmp__DateDebut__year=annee_en_cours, employee__CongEmp__Accepte=True, employee__CongEmp__type_conge='Congé de Maladie',  then=F('employee__CongEmp__duree')),default=0,
                output_field=DecimalField()
            )
        ),
    )
    
    dde_with_index = list(enumerate(dde))
    return render(request, 'conge_trait_dde.html', {'dde':dde_with_index,  } )

@staff_member_required
def trait_demande_conge_filtre(request,pk):
    annee_en_cours = ExtractYear(date.today())
    if pk:
        dde= PasserConge.objects.filter(id=pk)

        employes_avec_nombre_conges = dde.annotate(
        nombre_conges_annuels=Sum(
            Case(
                When(employee__CongEmp__DateDebut__year=annee_en_cours, employee__CongEmp__Accepte=True, employee__CongEmp__type_conge='Congé Annuel',  then=F('employee__CongEmp__duree')),default=0,
                output_field=DecimalField()
            )
        ),
        nombre_conges_maladie=Sum(
            Case(
                When(employee__CongEmp__DateDebut__year=annee_en_cours, employee__CongEmp__Accepte=True, employee__CongEmp__type_conge='Congé de Maladie',  then=F('employee__CongEmp__duree')),default=0,
                output_field=DecimalField()
            )
        ),
    )
    
    return render(request, 'conge_trait_dde _filtre.html', {'dde':employes_avec_nombre_conges,  } )


@staff_member_required
def conge_repondre(request,id,nbr):
    dde = get_object_or_404(PasserConge, id=id,Refuse=False,Accepte=False)
    traita = Compte.objects.filter(employee=dde.employee,annee = current_year())
    traita = traita.last()
    if (((dde.duree > dde.employee.nbrEmp.last().solde_conge) and (dde.type_conge == "Congé Annuel")) or
((dde.duree > dde.employee.nbrEmp.last().solde_conge_maladie) and (dde.type_conge == "Congé de Maladie"))) :
        messages.warning(request,"Attention solde congé dépassé..cette demande n'aurait pas dû être accepté ! test lors de la saisie de la demande à échoué ! effacez cette demande à partir de l'administration!")
        return redirect('admi:trait_demande_conge',)
    
    if nbr == 'acc'  :
        if (dde.type_conge == "Congé Annuel"):
# ((dde.duree > dde.employee.nbrEmp.last.solde_conge_maladie) and (dde.type_conge == "Congé de Maladie"))) :
            traita.solde_conge = traita.solde_conge - dde.duree
        
        else :
            traita.solde_conge_maladie = traita.solde_conge_maladie - dde.duree    
        dde.Accepte = True
        traita.save()
        
        
        dest=dde.employee.user.email
        subject = f"A propos de votre demande de congé"
        message = f"Ceci est un message automatique. N'y répondez pas.\n On vous informe que votre demande de congé "
        message += " du {} au {} " .format(dde.DateDebut.strftime("%d-%m-%Y"),dde.DateFin.strftime("%d-%m-%Y"))
        message += " a été accepté"
        send_mail(subject, message, settings.EMAIL_HOST_USER, [dest])        
        
        dde.save()
        messages.success(request,"Demande Accéptée. Solde congé mis à jour. Un mail à été envoyé ")
        return redirect('admi:trait_demande_conge')
    if nbr=="ref":
        
        dde.Refuse = True
       
        dde.save()


        
        dest=dde.employee.user.email
        subject = f"A propos de votre demande de congé"
        message = f"Ceci est un message automatique. N'y répondez pas.\n On vous informe que votre demande de congé "
        message += " du {} au {} " .format(dde.DateDebut.strftime("%d-%m-%Y"),dde.DateFin.strftime("%d-%m-%Y"))
        message += " a été refusé"
        send_mail(subject, message, settings.EMAIL_HOST_USER, [dest])
  



        messages.success(request,"Demande Refusée. Un mail à été envoyé ")
        return redirect('admi:trait_demande_conge')

    
    return render(request, 'conge_dde_confirm.html',{'id':id,'nbr':nbr,'dde':dde})

