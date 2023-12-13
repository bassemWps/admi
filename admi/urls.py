from django.shortcuts import render
from django.urls import path
from . import views
app_name = 'admi'
# Create your views here.
urlpatterns = [
path('', views.dashboard, name='dashboard'),
path('connexion/', views.user_login, name='connexion'),
path('deconnexion/', views.deconnexion, name='deconnexion'),
path('init_password/', views.changepassword, name='init_password'),    
path('register/', views.register, name='register'),   
path('employe/liste/', views.employe_list, name='employe_list'),
path('employe/<pk>/liste/', views.employe_list2, name='employe_list_filtre'),
path('employe/ajouter/', views.employe_ajouter.as_view(), name='employe_ajouter'),
path('employe/supprimer/<pk>/', views.employe_supprimer.as_view(),name='employe_supprimer'),
path('employe/<pk>/update', views.EmployeUpdateView.as_view(),name='employe_modifier'), 
path('employe/<pk>/deactivate', views.EmployeDesactivateView.as_view(),name='employe_deactiver'), 
path('employe/<pk>/conge', views.demander_conge,name='employe_conge'),
path('employe/<pk>/liste', views.liste_demander_conge,name='liste_demander_conge'),
path('employe/<pk>/<str:period>/liste', views.liste_demander_conge,name='liste_demander_conge_filtre'),
path('employe/traiter-demande', views.trait_demande_conge,name='trait_demande_conge'),
path('employe/<pk>/traiter-demande_filtre', views.trait_demande_conge_filtre,name='trait_demande_conge_filtre'),
path('employe/<str:id>/<str:nbr>/repondre-demande', views.conge_repondre,name='conge_repondre'),
]