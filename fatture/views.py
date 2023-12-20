import django.utils.timezone

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from datetime import datetime

from fatture.forms import ClienteForm, ViaggioForm, TassaForm, BurocraziaForm, UscitaForm, EntrataForm
from fatture.models import Fattura, Cliente, Viaggio
import pandas as pd

# Create your views here.

def fatture(request):

    mesiIta = {
        1: "Gennaio",
        2: "Febbraio",
        3: "Marzo",
        4: "Aprile",
        5: "Maggio",
        6: "Giugno",
        7: "Luglio",
        8: "Agosto",
        9: "Settembre",
        10: "Ottobre",
        11: "Novembre",
        12: "Dicembre",
    }


    fatture_list = Fattura.objects.all().order_by('-data')
    fatturato = 0
    spesaTot = 0
    km_percorsi = 0
    for fat in fatture_list:
        if fat.data.month == datetime.now().month:
            if fat.tipo == 'C':


                fatturato += fat.importo
            else:
                spesaTot += fat.importo

    for via in Viaggio.objects.all().filter(data_viaggio__month=django.utils.timezone.datetime.now().month):
        km_percorsi += via.distanza_km
    utile = fatturato - spesaTot
    spesaStimata = float(km_percorsi) / 4 * 1.85
    utileStimato = float(utile) - spesaStimata


    viaggi=Viaggio.objects.all()

    return render(request, 'fatture/index.html', {'fatture': fatture_list,
                                                  'viaggi':viaggi,
                                                      'fatturato': fatturato,
                                                      'spesaTot': spesaTot,
                                                      'utile': utile,
                                                      'mese': mesiIta[datetime.now().month],
                                                      'km_percorsi': km_percorsi,
                                                      'spesaStimata': spesaStimata,
                                                      'utileStimato': utileStimato})


def clienti(request):
    clienti_list = Cliente.objects.all().order_by('nome').exclude(nome='Inalca')
    viaggi_list = Viaggio.objects.filter(stato=0).order_by('-data_viaggio')

    if request.method == 'POST':
        if 'Aggiungi_Cliente' in request.POST:
            formC = ClienteForm(request.POST)
            if formC.is_valid():
                nuovo_cliente = formC.save()
            return redirect('clienti')
        if 'Aggiungi_Fattura' in request.POST:
            formF = EntrataForm(request.POST)
            if formF.is_valid():
                nuova_fattura = formF.save()
            return redirect('clienti')
        formV = ViaggioForm(request.POST)
        if formV.is_valid():
            nuovo_viaggio = formV.save()
        return redirect('clienti')
    else:
        formC = ClienteForm()
        formV = ViaggioForm()
        formF = EntrataForm()
        return render(request, 'fatture/clienti.html', {'formC': formC, 'formV': formV,'formF': formF, 'clienti': clienti_list, 'viaggi': viaggi_list})


def viaggi(request):
    clienti_list = Cliente.objects.all().filter(nome='Inalca')
    viaggi_list = Viaggio.objects.all().order_by('-data_viaggio')
    viaggi_list = viaggi_list.filter(cliente__nome='Inalca')
    if request.method == 'POST':
        if 'Aggiungi_Fattura' in request.POST:
            formF = EntrataForm(request.POST)
            if formF.is_valid():
                nuova_fattura = formF.save()
            return redirect('viaggi')
        form = ViaggioForm(request.POST, numero=1)
        if form.is_valid():
            nuovo_viaggio = form.save()
        return redirect('viaggi')
    else:
        form = ViaggioForm(numero=1)
        formF = EntrataForm()
        return render(request, 'fatture/viaggi.html', {'form': form, 'formF': formF, 'viaggi': viaggi_list, 'clienti': clienti_list})

def tassa(request):
    if request.method == 'POST':
        form = TassaForm(request.POST)
        if form.is_valid():
            nuova_fattura = form.save()

            return redirect('fatture')
    else:

        form = TassaForm()

        return render(request, 'fatture/crea/tassa.html', {'form': form})

def burocrazia(request):
    if request.method == 'POST':
        form = BurocraziaForm(request.POST)
        if form.is_valid():
            nuova_fattura = form.save()

            return redirect('fatture')
    else:

        form = BurocraziaForm()

        return render(request, 'fatture/crea/burocrazia.html', {'form': form})
def uscita(request):
    if request.method == 'POST':
        form = UscitaForm(request.POST)
        if form.is_valid():
            nuova_fattura = form.save()
            return redirect('fatture')
    else:

        form = UscitaForm()

        return render(request, 'fatture/crea/uscita.html', {'form': form})

def entrata(request, id):
    importo_finale = 0
    viaggi = Viaggio.objects.filter(cliente_id=id, stato=0)
    cliente = Cliente.objects.get(id=id)
    for viaggio in viaggi:
        importo_finale += viaggio.prezzo_viaggio
    if importo_finale == 0:
        return redirect('fatture')
    if request.method == 'POST':
        form = EntrataForm(request.POST, id=id)
        if form.is_valid():
            nuova_fattura = form.save()
            viaggi.update(stato=1)
            return redirect('fatture')
        else:
            # Se il form non è valido, potresti restituire un template renderizzato
            print(form.errors)
            return redirect('fatture')

    else:

        form = EntrataForm(id=id)


        return render(request, 'fatture/crea/cliente/entrata.html', {'form': form, 'cliente': cliente, 'viaggi':viaggi, 'importo': importo_finale})

def sceltaCliente(request):
    clienti = Cliente.objects.filter(
        viaggi_cliente__stato=0
    ).distinct()
    return render(request, 'fatture/crea/cliente/ScegliCliente.html',{'clienti': clienti})


def sceltaTipo(request):
    return render(request, 'fatture/crea/ScegliTipo.html')

def modifica(request, numero):
    fattura = Fattura.objects.get(numero=numero)
    print(fattura.viaggi.all())
    clienti = Cliente.objects.filter(
        viaggi_cliente__stato=0
    ).distinct()
    viaggi = Viaggio.objects.filter(stato=0)
    if request.method == 'POST':
        fattura.numero = request.POST['numero']
        fattura.data = request.POST['data']
        fattura.save()
        return redirect('fatture')

    return render(request, 'fatture/modifica.html',{'fattura': fattura,'clienti': clienti,'viaggi': viaggi,})

def elimina(request, numero):
    fattura = Fattura.objects.get(numero=numero)
    if request.method == 'POST':
        for viaggio in fattura.viaggi.all():
            viaggio.stato = 0
            viaggio.save()
        fattura.delete()
        return redirect('fatture')
    return render(request, 'fatture/elimina.html',{'fattura': fattura})

def eliminaV(request, id):
    viaggio = Viaggio.objects.get(id=id)
    try:
        fattura = Fattura.objects.get(viaggi=viaggio)
    except Fattura.DoesNotExist:
        fattura=None
    if fattura:
        fattura.importo -= viaggio.prezzo_viaggio
        if fattura.importo == 0:
            fattura.delete()
        else:
            fattura.save()
    if request.method == 'POST':
        viaggio.delete()
        if fattura:
            return JsonResponse({'success': True, 'importo_viaggio': viaggio.prezzo_viaggio, 'cliente_id':viaggio.cliente.id,'fattura_id': fattura.id,'fattura_numero':fattura.numero,'importo_f':fattura.importo})
        return JsonResponse(
            {'success': True, 'importo_viaggio': viaggio.prezzo_viaggio, 'cliente_id': viaggio.cliente.id,
             'viaggio_nome':viaggio.cliente.nome,'fattura_id': -1, 'fattura_numero': -1, 'importo_f': -1})
    return JsonResponse({'success': False})


def scegliViaggio(request):
    return render(request, 'fatture/ScegliViaggio.html')

def aggiornaPagato(request, id):
    if request.method == 'POST':
        viaggio = Viaggio.objects.get(id=id)
        pagato = viaggio.pagato
        pagato += 1
        pagato %= 2
        viaggio.pagato = pagato
        viaggio.save()
        return JsonResponse({'success': True, 'pagato': viaggio.pagato})
    print(request.method)
    return JsonResponse({'success': False})


def export_data_to_excel(request):
    objs = Fattura.objects.all()
    data = []

    for obj in objs:
        data.append({
            "numero": obj.numero,
            "data": obj.data,
            "importo": obj.importo,
            "tipo": obj.tipo,
            "cliente": obj.cliente,
            "numero": obj.numero,
        })
        for viaggio in obj.viaggi.all():
            data.append({
                "data": viaggio.data_viaggio,
                "ddt": viaggio.ddt,
                "prezzo": viaggio.prezzo_viaggio,
                "distanza": viaggio.distanza_km,
                "mittente": viaggio.mittente,
                "stato": viaggio.stato,
                "pagato": viaggio.pagato,

            })
        data.append({"":None})
    try:
        pd.DataFrame(data).to_excel("output.xlsx")
    except Exception:
        return JsonResponse({
        'status': 404
    })
    return JsonResponse({
        'status': 200
    })