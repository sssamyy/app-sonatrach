from django.urls import path
from . import views
urlpatterns = [
      path('creer_salle/', views.creer_salle, name='creer_salle'),
      path('salle/<int:salle_id>/', views.details_salle, name='details_salle'),
      path('SalleList/',views.list_salles, name='SalleList'),
      path('modifierSalle/<int:salle_id>/',views.modifier_salle, name='modifierSalle'),
      path('suprimmerSalle/<int:salle_id>/',views.supprimer_salle, name='supprimerSalle'),
 ]