from django.urls import path
from . import views


urlpatterns = [
    path('reservationList', views.liste_Demandes, name='reservation-list'),
    path('creer',views.demande_salle,name='reservation-create'),
    path('choixSalle/<int:pk>/', views.choisir_salle, name='reservation-choixSalle'),
    path('Confirmation/<int:pk>/',views.confirmer_demande,name='reservation-confirmation'),
    path('consulter_planning_salle/<int:rk>/<int:pk>/',views.index,name='consulter_planning_salle'),
    path('calendrier-salle/<int:pk>/',views.consulter_planning_salle,name='calendrier-salle'),
    path('ajouter_date/<int:rk>/<int:pk>/',views.ajouter_date,name='ajouter_date'),
    path('modifier_demande/<int:pk>/',views.modifier_demande,name='editDemande'),
    path('supprimer_demande/<int:pk>/',views.annuler_reservation,name='suppDemande'),
    path('list_demandes',views.afficher_demandes_admin,name='reservation-list-admin'),
    path('choisir_reponse/<int:pk>/',views.reponse_demande,name='reponseDemande'),
    path('list_reservation_traite',views.liste_reservation,name='reservation-list-traite'),
    #     Les pages d'admin
    
    path('reservations_traite',views.gerer_reservation_traite,name='reservation-list-traite-admin'),
    path('modifier_reservation/<int:pk>/',views.modifier_reservation,name='editReservation'),
    path('ajouter_reservation',views.ajouter_reservation,name='ajoutReservation'),

    #   les pages de superviseurs
    path('checkout/list/', views.checkout_list, name='checkout_list'),
    path('checkout/detail/<pk>/', views.CheckoutDetailView.as_view(), name='checkout_detail'),
    path('checkout/create/rapport/<pk>/', views.create_rapport, name='create_rapport'),
    path('rapport/list/', views.rapport_list, name='rapport_list'),
   
]
