from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey
from operator import itemgetter



class Patient(models.Model):
    first_name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)
    CIN=models.CharField(max_length=20)
    date_of_birth = models.DateField()

    def __str__(self):
        return str(self.id) + ") "+self.first_name +" "+  self.last_name + " "+ self.CIN


class Dossier(models.Model):
    Patient=ForeignKey(Patient,default=None,on_delete=CASCADE)
    fichier=models.FileField(upload_to='media')
    titre=models.CharField(max_length=30)
    def __str__(self):
        if self.titre!="":
            return self.titre
        else:
            return "fichier "+str(self.id)  

class Medecin(models.Model):
    CHOICES = [
        ('Immunologie','Immunologie'),
        ('Anesthésiologie','Anesthésiologie'),
        ('Andrologie','Andrologie'),
        ('Cardiologie',' Cardiologie'),
        ('Chirurgie cardiaque',' Chirurgie cardiaque'),
        ('Chirurgie esthétique,plastique et reconstructive','Chirurgie esthétique, plastique et reconstructive'),
        ('Chirurgie générale','Chirurgie générale'),
        ('Chirurgie maxillo-faciale','Chirurgie maxillo-faciale'),
        ('Chirurgie pédiatrique','Chirurgie pédiatrique'),
        ('Chirurgie thoracique','Chirurgie thoracique'),
        ('Chirurgie vasculaire','Chirurgie vasculaire'),
        ('Neurochirurgie','Neurochirurgie'),
        ('Dermatologie','Dermatologie'),
        ('Endocrinologie','Endocrinologie'),
        ('Gastro-entérologie','Gastro-entérologie'),
        ('Gériatrie','Gériatrie'),
        ('Gynécologie','Gynécologie'),
        ('Hématologie','Hématologie'),
        ('Hépatologie','Hépatologie'),
        ('Infectiologie','Infectiologie'),
        ('Néonatologie','Néonatologie'),
        ('Néphrologie','Néphrologie'),
        ('Neurologie',' Neurologie'),
        ('Odontologie','Odontologie'),
        ('Oncologie','Oncologie'),
        ('Obstétrique','Obstétrique'),
        ('Ophtalmologie','Ophtalmologie'),
        ('Orthopédie','Orthopédie'),
        ('Oto-rhino-laryngologie','Oto-rhino-laryngologie'),
        ('Pédiatrie','Pédiatrie'),
        ('Pneumologie','Pneumologie'),
        ('Psychiatrie','Psychiatrie'),
        ('Radiologie','Radiologie'),
        ('Radiothérapie','Radiothérapie'),
        ('Rhumatologie','Rhumatologie'),
        ('Urologie','Urologie'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    CIN=models.CharField(max_length=20)
    date_de_naissance=models.DateField()
    present = models.BooleanField(default=True)
    specialitee = models.CharField(max_length=70,choices=sorted(CHOICES, key=itemgetter(0)))
    image=models.ImageField(default=None,blank=True)
    numero=models.CharField(max_length=70)
    parcours=models.TextField(max_length=1000)
    email=models.EmailField(blank=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + " " + self.specialitee

class Receptionniste(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    present = models.BooleanField(default=True)
    CIN=models.CharField(max_length=20)
    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class salle_dattente(models.Model):
    doctor = models.ForeignKey(Medecin, on_delete=models.CASCADE)
    malade = models.ForeignKey(Patient, on_delete=models.CASCADE)
    active_case = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id)

class passage(models.Model):
    entrance = models.ForeignKey(salle_dattente, on_delete=models.CASCADE)
    act = models.BooleanField()
    temps_de_passage = models.DateTimeField()
    def __str__(self):
        return self.entrance.malade.first_name + " " + self.entrance.malade.last_name +" "+str(self.temps_de_passage)[:19]

class ppresent(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    test = models.BooleanField(default=True)

    def __str__(self):
        return str(self.patient)

class Messages(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    message = models.CharField(max_length=1200)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ('timestamp',)
