from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Patient, Medecin, salle_dattente, passage, Receptionniste,Dossier,ppresent

#admin.site.register(Patient)
admin.site.site_header='DoctorTalks'
#admin.site.register(User)
admin.site.unregister(Group)  


admin.site.register(salle_dattente)


# Register your models here.
class DossierAdmin(admin.StackedInline):
    model=Dossier


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display=('id','Prénom','Nom','CIN_','Date_de_naissance')
    def Prénom(self, obj):
        return obj.first_name
    def Nom(self, obj):
        return obj.last_name
    def Date_de_naissance(self, obj):
        return obj.date_of_birth

    def CIN_(self, obj):
        if obj.CIN !="":
            return obj.CIN 
        else:
            pass
    inlines=[DossierAdmin]
    class Meta:
        model=Patient

@admin.register(Medecin)
class MedecinAdmin(admin.ModelAdmin):
    list_display=('Prénom','Nom','CIN','Spécialité','Numéro')

    def Prénom(self, obj):
        return obj.user.first_name
    def Nom(self, obj):
        return obj.user.last_name
    def Spécialité(self, obj):
        return obj.specialitee
    def Numéro(self, obj):
        return obj.numero

@admin.register(Receptionniste)
class ReceptionnisteAdmin(admin.ModelAdmin):
    list_display=('Prénom','Nom','CIN')

    def Prénom(self, obj):
        return obj.user.first_name
    def Nom(self, obj):
        return obj.user.last_name

@admin.register(passage)
class passageAdmin(admin.ModelAdmin):
    list_display=('Patient','Médecin','temps_de_passage','type')

    def Patient(self, obj):
        return obj.entrance.malade.first_name+" "+obj.entrance.malade.last_name
    def Médecin(self, obj):
        return obj.entrance.doctor.user.first_name+" "+obj.entrance.doctor.user.last_name
    def type(self,obj):
        if obj.act:
            return "Entrée"
        else :
            return "Sortie"


@admin.register(Dossier)
class DossierAdmin(admin.ModelAdmin):
    list_display=('Patient_','CIN','titre','fichier')
    def Patient_(self, obj):
        return obj.Patient.first_name+" "+obj.Patient.last_name
    def CIN(self, obj):
        return obj.Patient.CIN

@admin.register(ppresent)
class ppresentAdmin(admin.ModelAdmin):
    list_display=('Prénom','Nom','CIN_','Date_de_naissance')
    def Prénom(self, obj):
        return obj.patient.first_name
    def Nom(self, obj):
        return obj.patient.last_name
    def Date_de_naissance(self, obj):
        return obj.patient.date_of_birth
    def CIN_(self, obj):
        if obj.patient.CIN !="":
            return obj.patient.CIN 
        else:
            return "-"
    