from django.shortcuts import render
from django.http import HttpResponseRedirect
from django_tables2 import RequestConfig
from client.models import Client, Client_Additional, Client_Warehouse
from client.tables import ClientTable, ClientWarehouseTable
from client.forms import ClientForm, ClientAdditionalForm, ClientWarehouseForm
from django.contrib.auth.decorators import login_required


@login_required(login_url='/login')
# Create your views here.
def client(request):
    table = ClientTable(Client.objects.all().select_related('addition'))
    RequestConfig(request, paginate={"per_page": 10}).configure(table)
    return render(request, 'client/client.html', {'table': table, 'model': 'client'})


def client_warehouse(request):
    table = ClientWarehouseTable(Client_Warehouse.objects.all())
    RequestConfig(request, paginate={"per_page": 10}).configure(table)
    return render(request, 'common/table.html', {'table': table, 'model': 'warehouse', 'url': '/client/warehouse/add'})


def get_client_warehouses(request):
    if request.is_ajax():
        warehouses = Client_Warehouse.objects.filter(client_id=request.GET['client'])
        return render(request, 'client/warehouses.html', {'warehouses': warehouses})


def add_client(request):
    if request.method == "POST":
        cform = ClientForm(request.POST, instance=Client())
        caform = ClientAdditionalForm(request.POST, instance=Client_Additional())

        if cform.is_valid() and caform.is_valid():
            client = cform.save(commit=False)
            client.awb_assigned_from = request.POST['client_code'] + '0000001'
            client.awb_assigned_to = request.POST['client_code'] + '0010000'
            client.awb_left = 10000
            client.save()
            instance = caform.save(commit=False)
            instance.client_id = client.pk
            instance.save()
            return HttpResponseRedirect('/client/')
    else:
        cform = ClientForm()
        caform = ClientAdditionalForm()
    return render(request, 'client/addclient.html', {'cform': cform, 'caform': caform})


def add_client_warehouse(request):
    if request.method == "POST":
        form = ClientWarehouseForm(request.POST, instance=Client_Warehouse())
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/client/warehouse')
    else:
        form = ClientWarehouseForm()
    return render(request, 'common/form.html', {'form': form, 'model': 'warehouse'})