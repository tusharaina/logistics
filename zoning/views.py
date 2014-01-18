from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django_tables2 import RequestConfig
from zoning.tables import CityTable, ZoneTable, PincodeTable
from zoning.models import City, Zone, Pincode
from zoning.forms import CityForm, ZoneForm, PincodeForm
from common.forms import ExcelUploadForm
from utils.upload import upload_pincode_city_file
from utils.upload import handle_uploaded_file
from logistics.settings import MEDIA_ROOT
from django.contrib.auth.decorators import login_required
import json


@login_required(login_url='/login')
# Create your views here.
def upload_file(request):
    if request.method == "POST":
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = handle_uploaded_file(request.FILES['file'], request.FILES['file'].name,
                                        MEDIA_ROOT + 'uploads/zoning/')
            upload_pincode_city_file(file)
            return HttpResponseRedirect('/internal/branch')
    else:
        form = ExcelUploadForm()
    return render(request, 'common/upload_form.html', {'form': form})


def city(request):
    table = CityTable(City.objects.all())
    RequestConfig(request, paginate={"per_page": 10}).configure(table)
    return render(request, 'zoning/city.html', {'table': table})


def add_city(request):
    if request.method == "POST":
        form = CityForm(request.POST, instance=City())
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/zoning/city')
    else:
        form = CityForm()
    return render(request, 'zoning/addcity.html', {'form': form})


def zone(request):
    table = ZoneTable(Zone.objects.all())
    RequestConfig(request, paginate={"per_page": 10}).configure(table)
    return render(request, 'zoning/zone.html', {'table': table})


def add_zone(request):
    if request.method == "POST":
        form = ZoneForm(request.POST, instance=Zone())
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/zoning/zone')
    else:
        form = ZoneForm()
    return render(request, 'zoning/addzone.html', {'form': form})


def pincode(request):
    table = PincodeTable(Pincode.objects.all())
    RequestConfig(request, paginate={"per_page": 10}).configure(table)
    return render(request, 'zoning/pincode.html', {'table': table})


def add_pincode(request):
    if request.method == "POST":
        form = PincodeForm(request.POST, instance=Pincode())
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/zoning/pincode')
    else:
        form = PincodeForm()
    return render(request, 'zoning/addpincode.html', {'form': form})


def pincode_search(request):
    term = request.GET.get('term') #jquery-ui.autocomplete parameter
    pincodes = Pincode.objects.filter(pincode__istartswith=term).order_by('pincode')[:10] #lookup for a city
    res = []
    for p in pincodes:
        #make dict with the metadatas that jquery-ui.autocomple needs (the documentation is your friend)
        dict = {'id': p.pk, 'label': p.pincode, 'value': p.pk}
        res.append(dict)
    return HttpResponse(json.dumps(res))