from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import ReservationForm,ReponseForm,ReservationAdminForm
from API.models import Reservation,Salle,Demande, Rapport
from django.core.paginator import Paginator
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.cache import never_cache
from django.views.generic import DetailView


# Create your views here
@never_cache
@login_required
def liste_Demandes(request):
    demandes=Demande.objects.filter(person_demande=request.user,etat_reservation='V')
    demande_heureFin=[]
    for d in demandes:
        demande_date_time=datetime.combine(d.dateReservation,d.heureDebutReservation)
        h=demande_date_time+d.dureeReservation
        h=h.time()
        demande_heureFin.append({'demande':d,'heure_fin':h})
    paginator=Paginator(demande_heureFin,10)
    page_number=request.GET.get("page")
    page_obj=paginator.get_page(page_number)
    template_name='listeDemandes.html'
    return render(request,template_name,{'page_obj':page_obj})

@login_required
def demande_salle(request):
    if request.method == 'POST':
        reservation_form = ReservationForm(request.POST)
        if reservation_form.is_valid():
            if request.session['reservation_existe']:
                reservation = Reservation.objects.get(idReservation=request.session['reservation'])
                reservation_form = ReservationForm(request.POST, instance=reservation)
                reservation_form.save()
            else:
                reservation=reservation_form.save(commit=False)
                reservation.person_demande=request.user
                reservation.save()
                reservation_form.save_m2m()  # Sauvegarde les services sélectionnés
                request.session['reservation_existe']=True
                request.session['reservation']=reservation.idReservation
                request.session['ad']=False
            return redirect('reservation-choixSalle',pk=reservation.idReservation)
    else:
        request.session['reservation_existe']=False
        if request.session['reservation_existe']:
            reservation=Demande.objects.get(idReservation=request.session['reservation'])
            reservation_form=ReservationForm(instance=reservation)
        else:
            reservation_form = ReservationForm()
    return render(request, 'creerDemande.html',{'reservation_form': reservation_form,})

@login_required
def choisir_salle(request,pk):
    reservation=Demande.objects.get(idReservation=pk)
    if request.method == 'POST':
        salle_id = request.POST.get('salle_id')
        salle=Salle.objects.get(id=salle_id)
        reservation.SalleReservation=salle
        reservation.save() 
        return redirect('reservation-confirmation',pk=reservation.idReservation)
    else:
        filters={}
        if reservation.typeSalleReservaiton:
            filters['typeSalle'] = reservation.typeSalleReservaiton
        if reservation.nbParticipant:
            filters['capacite__gte'] = reservation.nbParticipant
        salles=Salle.objects.filter(**filters)
        if reservation.dateReservation:
            reservation_datetime = datetime.combine(reservation.dateReservation, reservation.heureDebutReservation)
            heureFinReservation = reservation_datetime + reservation.dureeReservation
            heureFinReservation = heureFinReservation.time()
            salles_non_dispo=[]
            salles_dispo=[]
            salles_reserves=[]
            for salle in salles:
                reservations=Demande.objects.filter(dateReservation=reservation.dateReservation,SalleReservation=salle)
                is_disponible=True
                for r in reservations:
                    r_datetime=datetime.combine(r.dateReservation,r.heureDebutReservation)
                    heureFinReservation_r=r_datetime+r.dureeReservation
                    heureFinReservation_r=heureFinReservation_r.time()
                    condition1=(reservation.heureDebutReservation <= r.heureDebutReservation <= heureFinReservation)
                    condition2=(r.heureDebutReservation<=reservation.heureDebutReservation<=heureFinReservation_r)
                    if condition1 or condition2:
                        if r.etat_reservation=='C':
                            is_disponible=False
                            salles_non_dispo.append(salle)
                            break
                        elif r.etat_reservation=='V':
                            is_disponible=False
                            salles_reserves.append(salle)
                            break
                if is_disponible:
                    salles_dispo.append(salle)
            is_dateReservaiton=True
        else:
            salles_dispo=Salle.objects.all()
            is_dateReservaiton=False
        if request.session['ad']:
            base='baseadmin.html'
        else:
            base='base.html'
        return render(request, 'choixSalle.html', {'salles_dispo': salles_dispo,
                                                   'salles_reserves':salles_reserves,
                                                   'salles_non_dispo':salles_non_dispo,
                                                   'is_dateReservation':is_dateReservaiton,'reservation':pk,'base':base})

def index(request,rk,pk):
    salle=Salle.objects.get(id=pk)
    all_reservations=Demande.objects.filter(SalleReservation=salle)
    return render(request,'planning-salle.html',{'events':all_reservations,'id_reservation':rk,'id_salle':pk})

def consulter_planning_salle(request,pk):
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
def ajouter_date(request, rk,pk):
    if request.method == 'POST':
        date_reservation = request.POST.get('dateReservation')
        heure_debut_reservation = request.POST.get('heureDebutReservation')
        reservation = Reservation.objects.get(idReservation=rk)
        salle=Salle.objects.get(id=pk)
        reservation.dateReservation = date_reservation
        reservation.heureDebutReservation = heure_debut_reservation
        reservation.SalleReservation=salle
        reservation.save()
        return redirect('reservation-confirmation', pk=reservation.idReservation)
    else:
        return redirect('consulter_planning_salle', rk=pk, pk=reservation.SalleReservation.id)
@login_required
def confirmer_demande(request,pk):
    reservation=Demande.objects.get(idReservation=pk)
    if request.method == 'POST':
        if request.session['ad']:
            reservation.etat_reservation='C'
        else:
            reservation.etat_reservation='V'
        reservation.save()
        request.session['reservation_existe']=False
        if request.session['ad']:
            return redirect('reservation-list-traite-admin')
        else:
            return redirect('reservation-list')
    else:
        if request.session['ad']:
            base='baseadmin.html'
        else:
            base='base.html'
        return render(request,'confirmation.html',{'reservation':reservation,'base':base})

@login_required
def modifier_demande(request,pk):
    demande=Demande.objects.get(idReservation=pk)
    if request.method=='POST':
        reservation_form=ReservationForm(request.POST,instance=demande)
        if reservation_form.is_valid():
            if request.session['reservation_existe']:
                reservation = Reservation.objects.get(idReservation=request.session['reservation'])
                reservation_form = ReservationForm(request.POST, instance=reservation)
                reservation_form.save()
            else:
                reservation=reservation_form.save(commit=False)
                reservation.person_demande=request.user
                reservation.save()
                request.session['reservation_existe']=True
                request.session['reservation']=reservation.idReservation
            return redirect('reservation-choixSalle',pk=reservation.idReservation)
    else:
        request.session['reservation_existe']=False
        reservation_form=ReservationForm(instance=demande)
        return render(request,'modifier_reservation.html',{"reservation_form":reservation_form})

@login_required
def annuler_reservation(request,pk):
    reservation=Demande.objects.get(idReservation=pk)
    reservation.delete()
    return redirect('reservation-list')


# les views de l'admin

@login_required
def afficher_demandes_admin(request):
    demandes=Demande.objects.filter(etat_reservation='V').order_by('dateReservation','heureDebutReservation','DateDemande')
    demande_heureFin=[]
    for d in demandes:
        demande_date_time=datetime.combine(d.dateReservation,d.heureDebutReservation)
        h=demande_date_time+d.dureeReservation
        h=h.time()
        demande_heureFin.append({'demande':d,'heure_fin':h})
    paginator=Paginator(demande_heureFin,10)
    page_number=request.GET.get("page")
    page_obj=paginator.get_page(page_number)
    return render(request,'affichage_demande_admin.html',{'page_obj':page_obj})

@login_required
def reponse_demande(request,pk):
    demande=Reservation.objects.get(idReservation=pk)
    if request.method == 'POST':
        reponse_form = ReponseForm(request.POST)
        if reponse_form.is_valid():
            reponse=reponse_form.save(commit=False)
            reponse.reservationConcerne=demande
            reponse.save()
            demande_date_time=datetime.combine(demande.dateReservation,demande.heureDebutReservation)
            h=demande_date_time+demande.dureeReservation
            h=h.time()
            message = f"""
Bonjour {demande.person_demande.first_name} {demande.person_demande.last_name},

Nous avons le plaisir de vous informer que votre demande de réservation de salle a été acceptée.

Voici les détails de votre réservation :

Type de salle : {demande.typeSalleReservaiton}
Date de réservation : {demande.dateReservation}
Heure de début : {demande.heureDebutReservation}
Durée de la réservation : {demande.dureeReservation}
Nombre de participants : {demande.nbParticipant}
Salle réservée : {demande.SalleReservation}
Services inclus : {', '.join([str(service) for service in demande.services.all()])}
Équipements : Vidéoprojecteur , Tableau blanc

Nous sommes ravis de pouvoir répondre favorablement à votre demande et nous nous réjouissons de vous accueillir dans nos locaux.

N'hésitez pas à nous contacter si vous avez d'autres questions.

Cordialement."""
            send_mail(
                "reponse reservation",
                message,
                settings.EMAIL_HOST_USER,
                ["yanis.bouzid03@gmail.com"],
                fail_silently=False
            )
            return redirect('reservation-list-admin')  
    else:
        reponse_form = ReponseForm()
    return render(request, 'reponse_demande.html',{'form': reponse_form,'reservation':demande})

@login_required
def liste_reservation(request):
    reservations=Reservation.objects.filter(person_demande=request.user,etat_reservation__in=['C','A']).order_by('dateReservation','heureDebutReservation')
    reservation_heureFin=[]
    for d in reservations:
        demande_date_time=datetime.combine(d.dateReservation,d.heureDebutReservation)
        h=demande_date_time+d.dureeReservation
        h=h.time()
        reservation_heureFin.append({'reservation':d,'heure_fin':h})
    paginator=Paginator(reservation_heureFin,10)
    page_number=request.GET.get("page")
    page_obj=paginator.get_page(page_number)
    template_name='liste_reservation_traite.html'
    return render(request,template_name,{'page_obj':page_obj})

@login_required
def gerer_reservation_traite(request):
    reservations=Reservation.objects.filter(etat_reservation='C').order_by('dateReservation','heureDebutReservation')
    reservation_heureFin=[]
    for d in reservations:
        demande_date_time=datetime.combine(d.dateReservation,d.heureDebutReservation)
        h=demande_date_time+d.dureeReservation
        h=h.time()
        reservation_heureFin.append({'reservation':d,'heure_fin':h})
    paginator=Paginator(reservation_heureFin,10)
    page_number=request.GET.get("page")
    page_obj=paginator.get_page(page_number)
    template_name='reservation_traite_ad.html'
    return render(request,template_name,{'page_obj':page_obj})

@login_required
def modifier_reservation(request,pk):
    reservation=Reservation.objects.get(idReservation=pk)
    if request.method=='POST':
        reservation_form=ReservationForm(request.POST,instance=reservation)
        if reservation_form.is_valid():
            if request.session['reservation_existe']:
                reservation = Reservation.objects.get(idReservation=request.session['reservation'])
                reservation_form = ReservationForm(request.POST, instance=reservation)
                reservation_form.save()
            else:
                reservation=reservation_form.save(commit=False)
                reservation.person_demande=request.user
                reservation.save()
                request.session['reservation_existe']=True
                request.session['reservation']=reservation.idReservation
            return redirect('reservation-choixSalle',pk=reservation.idReservation)
    else:
        request.session['reservation_existe']=False
        reservation_form=ReservationForm(instance=reservation)
        return render(request,'modifier_reservation.html',{"reservation_form":reservation_form})

@login_required
def ajouter_reservation(request):
    if request.method == 'POST':
        reservation_form = ReservationAdminForm(request.POST)
        if reservation_form.is_valid():
            if request.session['reservation_existe']:
                reservation = ReservationAdminForm.objects.get(idReservation=request.session['reservation'])
                reservation_form = ReservationAdminForm(request.POST, instance=reservation)
                reservation_form.save()
            else:
                reservation=reservation_form.save()
                request.session['reservation_existe']=True
                request.session['reservation']=reservation.idReservation
                request.session['ad']=True
            return redirect('reservation-choixSalle',pk=reservation.idReservation)
    else:
        request.session['reservation_existe']=False
        if request.session['reservation_existe']:
            reservation=Reservation.objects.get(idReservation=request.session['reservation'])
            reservation_form=ReservationAdminForm(instance=reservation)
        else:
            reservation_form = ReservationAdminForm()
    return render(request, 'ajouter_reservation.html',{'reservation_form': reservation_form,})
@login_required
def checkout_list(request):
    demandes = Demande.objects.filter(etat_reservation='A').order_by('-dateReservation')
    return render(request, 'checkout_list.html', {'demandes': demandes})

class CheckoutDetailView( DetailView):
    model = Demande
    template_name = 'checkout_detail.html'

@login_required
def create_rapport(request, pk):
    demande = Demande.objects.get(pk=pk)
    if request.method == 'POST':
        form = RapportForm(request.POST)
        if form.is_valid():
            rapport = form.save(commit=False)
            rapport.demande = demande
            rapport.save()
            demande.etat_reservation = 'F'
            demande.save()
            return redirect('checkout_list')
    else:
        form = RapportForm()
    return render(request, 'checkout_form.html', {'form': form, 'demande': demande})
@login_required
def rapport_list(request):
    rapports = Rapport.objects.all()
    return render(request, 'rapport_list.html', {'rapports': rapports})