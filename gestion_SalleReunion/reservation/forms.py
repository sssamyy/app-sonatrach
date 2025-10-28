from django import forms
from API.models import Reservation,Demande,Service,TypeEquipement, Rapport
from django.forms.widgets import TimeInput
from datetime import timedelta,date,datetime,time



class ReservationForm(forms.ModelForm):
    typeSalleReservaiton=forms.ChoiceField(choices=[
        ('Salle Réunion', 'Salle Réunion'),
        ('Amphie', 'Amphie'),
        ('Salle étranger', 'Salle étranger'),
    ],label='Type de Salle')
    dateReservation = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),required=True,label='Date de Réservation')
    heureDebutReservation = forms.TimeField( widget=TimeInput(format='%H:%M', attrs={'type': 'time','id':'heureDebutReservation'}),required=True,label='Heure de Debut de Réservation')
    DUREE_CHOICES = (
        (timedelta(hours=1), '1 heure'),
        (timedelta(hours=1, minutes=30), '1 heure 30 minutes'),
        (timedelta(hours=2), '2 heures'),
        (timedelta(hours=2, minutes=30), '2 heures 30 minutes'),
        (timedelta(hours=3), '3 heures'),
        (timedelta(hours=3, minutes=30), '3 heures 30 minutes'),
        (timedelta(hours=4), '4 heures'),
        (timedelta(hours=4, minutes=30), '4 heures 30 minutes'),
        (timedelta(hours=5), '5 heures'),
        (timedelta(days=1), 'Toute la journée'),
    )
    dureeReservation = forms.ChoiceField(choices=DUREE_CHOICES, label='Durée de la réservation',widget=forms.Select(attrs={'id':'dureeReservation'}))
    nbParticipant = forms.IntegerField(min_value=1, label='Nombre de participants',widget=forms.NumberInput(attrs={'id':'gg'}))
    services = forms.ModelMultipleChoiceField(
        queryset=Service.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    equipements=forms.ModelMultipleChoiceField(
        queryset=TypeEquipement.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    def clean(self):
        cleaned_data = super().clean()
        dateReservation = cleaned_data.get('dateReservation')
        heureDebutReservation = cleaned_data.get('heureDebutReservation')
        if dateReservation and dateReservation < date.today():
            self.add_error('dateReservation', "La date de réservation doit être supérieure ou égale à la date d'aujourd'hui.")
        elif dateReservation and heureDebutReservation and dateReservation == date.today() and heureDebutReservation < datetime.now().time():
            self.add_error('heureDebutReservation', "L'heure de début de la réservation doit être supérieure à l'heure actuelle.")
        return cleaned_data
    
    class Meta:
        model=Demande
        fields=['typeSalleReservaiton','dateReservation','heureDebutReservation','dureeReservation','nbParticipant','services',]
        

class ReponseForm(forms.ModelForm):
    Status_choices=(
        ('Valider','Valider'),('Annuler','Annuler')
    )
    Status=forms.CharField(widget=forms.RadioSelect(attrs={'id':'id_Status'},choices=Status_choices))
    cause=forms.CharField(widget=forms.Textarea,required=False)
    class Meta:
        model=Reservation
        fields=['Status','cause']

class ReservationAdminForm(forms.ModelForm):
    typeSalleReservaiton=forms.ChoiceField(choices=[
        ('Salle Réunion', 'Salle Réunion'),
        ('Amphie', 'Amphie'),
        ('Salle étranger', 'Salle étranger'),
    ],label='Type de Salle')
    dateReservation = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),required=True,label='Date de Reservation')
    heureDebutReservation = forms.TimeField( widget=TimeInput(format='%H:%M', attrs={'type': 'time','id':'heureDebutReservation'}),required=True,label='Heure de Debut de Reservation')
    DUREE_CHOICES = (
        (timedelta(hours=1), '1 heure'),
        (timedelta(hours=1, minutes=30), '1 heure 30 minutes'),
        (timedelta(hours=2), '2 heures'),
        (timedelta(hours=2, minutes=30), '2 heures 30 minutes'),
        (timedelta(hours=3), '3 heures'),
        (timedelta(hours=3, minutes=30), '3 heures 30 minutes'),
        (timedelta(hours=4), '4 heures'),
        (timedelta(hours=4, minutes=30), '4 heures 30 minutes'),
        (timedelta(hours=5), '5 heures'),
        (timedelta(days=1), 'Toute la journée'),
    )
    dureeReservation = forms.ChoiceField(choices=DUREE_CHOICES, label='Durée de la réservation',widget=forms.Select(attrs={'id':'dureeReservation'}))
    nbParticipant = forms.IntegerField(min_value=1, label='Nombre de participants',widget=forms.NumberInput(attrs={'id':'gg'}))
    visuoConference = forms.BooleanField(
        required=False,
        label='Visio-conférence'
    )
    def clean(self):
        cleaned_data = super().clean()
        dateReservation = cleaned_data.get('dateReservation')
        heureDebutReservation = cleaned_data.get('heureDebutReservation')
        if dateReservation and dateReservation < date.today():
            self.add_error('dateReservation', "La date de réservation doit être supérieure ou égale à la date d'aujourd'hui.")
        elif dateReservation and heureDebutReservation and dateReservation == date.today() and heureDebutReservation < datetime.now().time():
            self.add_error('heureDebutReservation', "L'heure de début de la réservation doit être supérieure à l'heure actuelle.")
        return cleaned_data
    
    class Meta:
        model=Reservation
        exclude=('DateDemande','SalleReservation','etat_reservation')

class RapportForm(forms.ModelForm):
    class Meta:
        model = Rapport
        fields = ('situationReservation', 'commentaire')