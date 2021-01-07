from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from rest_framework.fields import CurrentUserDefault
from accounts.models import Patient, Medecin, salle_dattente, passage, Receptionniste, Messages,Dossier, ppresent
from .forms import SignUpForm
from datetime import datetime
from django.http import JsonResponse
from django.views import View
from django.utils import formats
from accounts.serializers import MessageSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser





def check(request):
    act = Receptionniste.objects.all()
    if request.user.is_authenticated:
         id_p = request.user.id
         test = False
         for a in act:
            if a.user.id == id_p:
                test = True
                return HttpResponseRedirect(reverse("reception")) 
         if test is False:
                p=Patient.objects.all()
                m = Medecin.objects.all()
                s = salle_dattente.objects.all()
                return render(request, 'dashboard.html',{'Patients':p,'Medecin': m, 'salle_dattente': s})
    else:
         return render(request, "registration/login.html")



def handler404(request,exception):
    if exception:
        print('ok')
        return render(request, '404.html', status=404)
        
    


def login_view(request):
    act = Receptionniste.objects.all()
    med = Medecin.objects.all()
    p=Patient.objects.all()
    m = Medecin.objects.all()
    s = salle_dattente.objects.all()
    if request.method == "POST":
            # Attempt to sign user in
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)

            # Check if authentication successful
            if user is not None:
                login(request, user)
                id_p = request.user.id
                test = False
                for a in act:
                    if a.user.id == id_p:
                        test = True
                        return HttpResponseRedirect(reverse("reception")) 
                for me in med :
                    if me.user.id == id_p:
                        test = True
                        return render(request, 'dashboard.html',{'Patients':p,'Medecin': m, 'salle_dattente': s})
                if test is False:
                    return HttpResponseRedirect(reverse("to_admin"))
            else:
                info = "Invalid username and/or password."
                return render(request, "registration/login.html", {
                "info": info 
            })
    else:
        return render(request, "registration/login.html")


    



#@login_required
def dashboard(request):
    if (request.user.is_authenticated):
        med = Medecin.objects.all()
        t = False
        for m in med:
            if (m.user.id == request.user.id):
                p=Patient.objects.all()
                m = Medecin.objects.all()
                s = salle_dattente.objects.all()
                t = True
                return render(request, 'dashboard.html',{'Patients':p,'Medecin': m, 'salle_dattente': s})
        if (t == False):
            return render(request, "reception/error.html")
    else:
        return render(request, "reception/error.html")






def searche(request):
    return render(request,"registration/search.html")





def profile(request):
    m=Medecin.objects.get(user=request.user)
    return render(request,"registration/profile.html",{"medecin":m})





def search(request):
    if(request.POST):
        data1 = request.POST.get('texto1')
        data2 = request.POST.get('texto2')
        data=data1+data2
        p=Patient.objects.all()
        m = Medecin.objects.all()
        s = salle_dattente.objects.all()
        clear=False        
        print(data)
        try:
            id_pat =int( data )
            cryptbase1= 12345678909876
            cryptbase2= 234567890987654 
            id_pat = (id_pat ^ cryptbase2) - cryptbase1
            id_pat = Patient.objects.get(id=id_pat)
        except Exception:
            print("entrer un id valid")
            return render(request, "registration/search.html")

        for pres in ppresent.objects.all():
            if pres.patient== id_pat:
                clear=True
                break
        if not clear:
            return render(request, "registration/search.html")
        id_med = request.user.id
        id_med = Medecin.objects.get(user = id_med)
        b = salle_dattente(doctor = id_med, malade = id_pat)
        clear=True
        for k in s:
            if b.doctor==k.doctor and b.malade==k.malade and k.active_case:
                clear=False
        
        if clear or s.count()==0:
            b.save()
            s = salle_dattente.objects.all()
        date_joined = datetime.now()
        formatted_datetime = formats.date_format(date_joined, "SHORT_DATETIME_FORMAT")
        print(formatted_datetime)
        try:
            data=int(data)
        except Exception :
            print("entrer un id valid")
        return render(request, 'dashboard.html', {'data': data,'Patients':p, 'Medecin': m, 'salle_dattente': s})
    else:
        return render(request, "registration/search.html")





def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})





def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})




def passaging(request, salle):
    walk_test = passage.objects.all()
    nbr = int(salle)
    room = salle_dattente.objects.get(id = nbr)
    s = salle_dattente.objects.all()
    if(request.POST):
        num=passage.objects.filter(entrance=room).count()
        if num%2==0:
            b = passage(entrance = room,act = True , temps_de_passage = datetime.now())
        else :
            b = passage(entrance = room,act = False , temps_de_passage = datetime.now())
        b.save()
        return render(request, "registration/passage.html", {'walk_test':walk_test, 'nbr':nbr,'salle_dattente': s})
    if salle is None:
        return render(request, "registration/error.html")
    else:
        return render(request, "registration/passage.html", {'walk_test':walk_test, 'nbr':nbr,'salle_dattente': s})






def information(request, nbr):
    s = salle_dattente.objects.all()
    br = int(nbr)
    print(br)
    p=salle_dattente.objects.get(id=br).malade
    dossier=Dossier.objects.filter(Patient = p)
    if(request.POST):
        i1=request.POST.get('titre')
        i2=request.FILES['fichier']
        doc=Dossier(Patient=Patient.objects.get(id=p.id),titre=i1,fichier=i2)
        doc.save()
        return render(request, "registration/information.html" ,{'nbr':br,'salle_dattente': s,'dossier':dossier,'Pat':p})
    else:
        return render(request, "registration/information.html" ,{'nbr':br,'salle_dattente': s,'dossier':dossier,'Pat':p})






def reception(request):
    return render(request, "reception/check_in.html")






def search_recep1(request, choix):
    global id_patient
    if(request.POST):
        if choix == "1":
            info = request.POST.get('text')
            try:
                info=int(info)
                cryptbase1= 12345678909876
                cryptbase2= 234567890987654
                info = (info ^ cryptbase2) - cryptbase1
                id_patient = Patient.objects.filter(id = info) 
                if ppresent.objects.filter(patient=Patient.objects.get(id=id_patient.first().id)).count()!=0:
                    warning = "Cette personne est déjà présente dans l'hôpital !"
                    return render(request, "reception/search_id.html", {'warning': warning, 'choix': choix})  
            except Exception :
                warning = "Aucun résultat !"
                return render(request, "reception/search_id.html", {'warning': warning, 'choix': choix})
            
            else:
                return render(request, 'reception/check_in.html', {'id_patient': id_patient})
        elif choix == "2":
            info = request.POST.get('text2')
            print(info)
            ps=Patient.objects.all()
            liste=[]
            for p in ps:
                if info.lower() in (p.first_name+p.last_name).lower():
                    liste.append(p)
            print(liste)

            if liste==[]:
                warning = "Aucun résultat !"
                return render(request, "reception/search_id.html", {'warning': warning, 'choix': choix})
            id_patient=liste
            return render(request, 'reception/check_in.html', {'id_patient': id_patient})
        elif choix == "3":
            info = request.POST.get('text3')
            try:
                id_patient = Patient.objects.filter(CIN = info)
            except Exception :
                warning = "Aucun résultat !"
                return render(request, "reception/search_id.html", {'warning': warning, 'choix': choix})
            return render(request, 'reception/check_in.html', {'id_patient': id_patient})
    else:
        if choix == "1":
            return render(request, "reception/search_id.html", {'choix': choix})
        if choix == "2":
            return render(request, "reception/search_id.html", {'choix': choix})
        if choix == "3":
            return render(request, "reception/search_id.html", {'choix': choix})
        else:
            return render(request, "reception/error.html")






def search_recep2(request, choix):
    global id_patient
    if(request.POST):
        if choix == "1":
            info = request.POST.get('text')
            try:
                info=int(info)
                cryptbase1= 12345678909876
                cryptbase2= 234567890987654
                info = (info ^ cryptbase2) - cryptbase1
                id_patient=ppresent.objects.filter(patient=Patient.objects.get(id = info))
                print(id_patient)
            except Exception :
                warning = "Cet ID ne figure pas dans la base de données !"
                return render(request, "reception/search_id.html", {'warning': warning, 'choix': choix})
            if id_patient.count()==0:
                warning = "La personne possedant cet ID n'a pas fait de le check in !"
                return render(request, "reception/search_id.html", {'warning': warning, 'choix': choix})

            return render(request, 'reception/checkout.html', {'id_patient': id_patient})
        elif choix == "2":
            info = request.POST.get('text2')
            print(info)
            ps=ppresent.objects.all()
            liste=[]
            for p in ps:
                if info.lower() in (p.patient.first_name+p.patient.last_name).lower():
                    liste.append(p)
            print(liste)

            if liste==[]:
                warning = "Aucun résultat !"
                return render(request, "reception/search_out.html", {'warning': warning, 'choix': choix})
            id_patient=liste
            return render(request, 'reception/checkout.html', {'id_patient': id_patient})
        elif choix == "3":
            info = request.POST.get('text3')
            
            try:
                id_patient = ppresent.objects.filter(patient = Patient.objects.filter(CIN=info).first())
            except Exception :
                warning = "enter a valid CIN"
                return render(request, "reception/search_id.html", {'warning': warning, 'choix': choix})
            return render(request, 'reception/checkout.html', {'id_patient': id_patient})
    else:
        if choix == "1":
            return render(request, "reception/search_out.html", {'choix': choix})
        if choix == "2":
            return render(request, "reception/search_out.html", {'choix': choix})
        if choix == "3":
            return render(request, "reception/search_out.html", {'choix': choix})
        else:
            return render(request, "reception/error.html")




def chekedin(request, idd):
    p = Patient.objects.get(id = idd)
    x=ppresent.objects.filter(patient=p)
    if ppresent.objects.filter(patient=p).count()==0:
        pp = ppresent(patient=p)
        pp.save()
        p.present = True
        p.save()
        return HttpResponseRedirect(reverse("reception"),{'message':"L'entrée du patient est enregistrée !"})   
    else:
        return render(request, "reception/check_in.html",{'message':"Cette personne est déjà présente dans l'hôpital !"})




def checkout(request):
        pp = ppresent.objects.all()
        return render(request, "reception/checkout.html", {'pp': pp})






def checkout2(request, id1,id2):
    salles=salle_dattente.objects.filter(malade=Patient.objects.get(id =id1))
    print(salles)
    for salle in salles:
        salle.active_case=False
        salle.save()
    pp = ppresent.objects.filter(patient =Patient.objects.get(id =id1)).first()
    pp.delete()
    return HttpResponseRedirect(reverse("checkout"),{'message':"La sortie du patient est enregistrée !"})







def patient_info(request,idP):
    pat=Patient.objects.filter(id=idP)
    print(idP)
    cryptbase1= 12345678909876
    cryptbase2= 234567890987654
    id_crypte = (int(idP)+ cryptbase1) ^ cryptbase2
    return render(request, "reception/patient_info.html", {'patient': pat,'id_patient':id_patient,'id_crypte':id_crypte})







def patient_info_p(request,idP):
    global id_patient
    pat=Patient.objects.filter(id=idP)
    return render(request, "reception/patient_info_p.html", {'patient': pat,'id_patient':id_patient})






def patcreat(request):
    if (request.POST):
        i1 = request.POST.get('nom')
        i2 = request.POST.get('prenom')
        i3 = request.POST.get('date_de_N')
        i4 = request.POST.get('CIN')
        p = Patient.objects.all()
        pp=ppresent.objects.all()
        try:
            nom = i1
            prenom = i2
            birthday = i3
            numCIN = i4
            b = Patient(first_name=prenom, last_name=nom, CIN=numCIN, date_of_birth=birthday)
            b.save()
            bp=ppresent(patient=b)
            bp.save()
        except Exception :
            print("respecter les champs")
        return render(request, 'reception/check_in.html',{'message':"Le patient est enregistré !"})
    else:
        return render(request, "reception/creation.html")










#----------------------------------------test code -------- version non stable -------------------




@csrf_exempt
def message_list(request, sender=None, receiver=None):
    """
    List all required messages, or create a new message.
    """
    if request.method == 'GET':
        messages = Messages.objects.filter(sender_id=sender, receiver_id=receiver, is_read=False)
        serializer = MessageSerializer(messages, many=True, context={'request': request})
        for message in messages:
            message.is_read = True
            message.save()
            
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            print("message save")
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)





def chat_view(request):
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "GET":
        if  request.user.is_authenticated:
            idd = request.user.id
            u = User.objects.get(id = idd)
            p = Medecin.objects.get(user = u )
            p = p.id
            return render(request, 'chat/chat.html',
                        {'users': User.objects.exclude(username=request.user.username),
                        'Medecin': Medecin.objects.exclude(id=p)})





def message_view(request, sender, receiver):
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "GET":
        idd = request.user.id
        u = User.objects.get(id = idd)
        p = Medecin.objects.get(user = u )
        p = p.id
        return render(request, "chat/messages.html",
                      {'users': User.objects.exclude(username=request.user.username),
                       'receiver': User.objects.get(id=receiver),
                       'Medecin': Medecin.objects.exclude(id=p),
                       'messages': Messages.objects.filter(sender_id=sender, receiver_id=receiver) |
                                   Messages.objects.filter(sender_id=receiver, receiver_id=sender)})



            




    