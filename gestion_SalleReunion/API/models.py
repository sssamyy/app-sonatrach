from django.db import models
from datetime import timedelta
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class TypeEquipement(models.Model):
    idEquipement=models.AutoField(primary_key=True)
    nomEquipment=models.CharField(max_length=30)
    def __str__(self):
        return self.nomEquipment
    class Meta :
       db_table="TypeEquipement"
    
class Salle(models.Model):
    etage = models.PositiveSmallIntegerField( default=0)
    zone = models.PositiveSmallIntegerField( default=1)
    numero_de_salle = models.CharField(max_length=100)
    nom_salle=models.CharField(max_length=50,null=True)
    id=models.AutoField(primary_key=True)
    capacite=models.IntegerField(blank=False)
    etat=models.CharField(max_length=50)
    typeSalle=models.CharField(max_length=30)
    equiments_salle=models.ManyToManyField('TypeEquipement',related_name='salles')
    securise=models.BooleanField(default=False) 
    def __str__(self):
        if self.nom_salle:
            return self.nom_salle
        else:
            return  f"Salle {self.numero_de_salle}"
    class Meta :
        db_table="salle"
    




class Demande(models.Model):
    idDemande=models.AutoField(primary_key=True)
    DateDemande=models.DateTimeField(auto_now_add=True)
    SalleReservation=models.ForeignKey(Salle,on_delete=models.SET_NULL,null=True,related_name='reservations')
    dateReservation =models.DateField(null=True)
    heureDebutReservation=models.TimeField(null=True)
    dureeReservation=models.DurationField(default=timedelta(hours=1),null=True)
    nbParticipant=models.IntegerField(null=True)
    services=models.ManyToManyField('Service',related_name='Reservation')
    equipments=models.ManyToManyField('TypeEquipement',related_name='demandes')
    typeSalleDemande=models.CharField(max_length=30,null=True)
    person_demande=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    etat_reservation=models.CharField(default='E',max_length=1)
    class Meta :
        db_table="Demande"

class Service(models.Model):
    idService=models.AutoField(primary_key=True)
    nomService=models.CharField(max_length=30)
    class Meta:
        db_table="Service"
    def __str__(self):
        return self.nomService

class Reservation(models.Model):
    idReservation=models.AutoField(primary_key=True)
    status=models.CharField(max_length=20)
    reservationConcerne=models.OneToOneField(Demande,on_delete=models.CASCADE)
    commentaire=models.TextField(null=True)
    class Meta:
        db_table="Reservation"

class Rapport(models.Model):
    idRapport=models.AutoField(primary_key=True)
    dateRapport=models.DateField()
    situationReservation=models.CharField(max_length=30)
    commentaire=models.TextField()
    class Meta:
        db_table="Rapport"