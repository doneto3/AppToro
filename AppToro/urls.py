"""
URL configuration for AppToro project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django_select2.views import AutoResponseView

from fatture import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('fatture/', views.fatture, name="fatture"),
    path('clienti/', views.clienti, name="clienti"),
    path('viaggi/', views.viaggi, name="viaggi"),
    path('creaFattura/', views.sceltaTipo, name="sceltaTipo"),
    path('creaFattura/Burocrazia', views.burocrazia, name="burocrazia"),
    path('creaFattura/Tassa', views.tassa, name="tassa"),
    path('creaFattura/Cliente', views.sceltaCliente, name="sceltaCliente"),
    path('creaFattura/Uscita', views.uscita, name="uscita"),
    path('creaFattura/Cliente/<int:id>', views.entrata, name="entrata"),
    path('modifica/<int:numero>', views.modifica, name="modifica"),
    path('elimina/<int:numero>', views.elimina, name="elimina"),
    path('eliminaV/<int:id>', views.eliminaV, name="eliminaV"),
    path('aggiornaPagato/<int:id>', views.aggiornaPagato, name="aggiornaPagato"),
    path('scegliViaggio', views.scegliViaggio, name="scegliViaggio"),
    path('excel/', views.export_data_to_excel, name="excel"),
    path('eliminaC/<int:id>', views.eliminaC, name="eliminaC"),
]
