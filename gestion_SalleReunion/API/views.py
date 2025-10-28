from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth import login,logout
import datetime
from django.views.decorators.cache import never_cache
from django.contrib.auth.views import LoginView
from API.models import Reservation,Salle
from django.contrib.auth.decorators import login_required



# Create your views here.


@never_cache
@login_required
def dashbord_user(request):
    return render(request,'dashbordUser.html')

@login_required
def dashbord_admin(request):
    nb_demande=Reservation.objects.filter(etat_reservation='V').count()
    return render(request,'dashbordAdmin.html',{'nb_demande':nb_demande})

def index_planning(request):
    return render(request,'planning.html')

def calendar_view(request,pk):
    out=[]
    salle=Salle.objects.get(id=pk)
    reservation=Reservation.objects.filter(SalleReservation=salle,etat_reservation='C')
    for r in reservation:
        date_heure_debut=datetime.combine(r.dateReservation,r.heureDebutReservation)
        date_heure_fin=datetime.combine(r.dateReservation,r.heureDebutReservation)+r.dureeReservation
        out.append({
            'title':r.idReservation,
            'id': r.idReservation,
            'start':date_heure_debut.isoformat(),
            'end':date_heure_fin.isoformat()
        })
    return JsonResponse(out,safe=False)

class AuthenticationView(LoginView):
    template_name = 'login.html'

    def form_valid(self, form):
        """
        Méthode appelée lorsque le formulaire de connexion est valide.
        """
        user = form.get_user()
        login(self.request, user)
        if user.is_superuser:
            return redirect('dashbord_admin')
        if user.is_staff:
            return redirect('dashbord_user')
        

    def form_invalid(self, form):
        """
        Méthode appelée lorsque le formulaire de connexion est invalide.
        """
        return render(self.request, 'login.html', {'erreur': 'Identifiant ou mot de passe invalide'})

@never_cache
def logout_view(request):
    logout(request)
    return redirect('authentification')