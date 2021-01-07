from django.urls import path
from . import views as views
from django.contrib.auth.views import  LogoutView
from django.views.static import serve
from django.conf.urls import url
import os
from django.contrib import admin
from django.urls import path, reverse_lazy
from django.views.generic.base import RedirectView
from django.conf.urls import handler404

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
handler404 = views.handler404

urlpatterns = [
    path('dashboard/',views.dashboard, name='dashboard'),
    path('', views.check, name='check'),
    path('login/', views.login_view, name='login'),
    path('logout/',LogoutView.as_view(next_page='login'), name="logout_url"),
    path('search/', views.search, name="search"),
    path('profile/', views.profile, name="profile"),
    path('signup/',views.signup, name='signup'),
    path("patient/<str:salle>", views.passaging, name="salle"),
    path("patient/<str:nbr>/information", views.information, name="info"),
    path('reception/', views.reception, name="reception"),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/<str:id1>/<str:id2>', views.checkout2, name='checkout2'),
    path('chekedin/<str:idd>', views.chekedin, name="chekedin"),
    path('recherche_recep1/<str:choix>', views.search_recep1, name="recherche_recep1"),
    path('recherche_recep2/<str:choix>', views.search_recep2, name="recherche_recep2"),
    path("recherche_recep1/patient_info/<str:idP>",views.patient_info, name="patient_info"),
    path("recherche_recep2/patient_info_p/<str:idP>",views.patient_info_p, name="patient_info_p"),
    path('patcreation/', views.patcreat, name='patcreation'),
    # Serve up a local static folder to serve spinner.gif
    url(r'^static/(?P<path>.*)$', serve,
        {'document_root': os.path.join(BASE_DIR, 'static'), 'show_indexes': True},
        name='static'
    ),
    path('chat/', views.chat_view, name='chats'),
    path('chat/<int:sender>/<int:receiver>/', views.message_view, name='chat'),
    path('api/messages/<int:sender>/<int:receiver>/', views.message_list, name='message-detail'),
    path('api/messages/', views.message_list, name='message-list'),
    path('uu/', RedirectView.as_view(url=reverse_lazy('admin:index')),name='to_admin'),
    path('admin/', admin.site.urls),
    
    


]   