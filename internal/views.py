import re

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django_tables2 import RequestConfig
from django.contrib.auth.decorators import login_required

from internal.tables import BranchTable, EmployeeTable, VehicleTable, BranchPincodeTable
from internal.models import Branch, Employee, Vehicle, Branch_Pincode
from internal.forms import BranchForm, EmployeeForm, VehicleForm, BranchPincodeForm, BranchDropDownForm
from common.forms import ExcelUploadForm
from utils.upload import handle_uploaded_file, upload_branch_pincode_file, upload_vehicle_list_file
from logistics.settings import MEDIA_ROOT


@login_required(login_url='/login')
# Create your views here.
def branch(request):
    table = BranchTable(Branch.objects.all())
    RequestConfig(request, paginate={"per_page": 10}).configure(table)
    return render(request, 'internal/branch.html', {'table': table})


def add_branch(request):
    if request.method == "POST":
        form = BranchForm(request.POST, instance=Branch())
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/internal/branch')
    else:
        form = BranchForm()
    return render(request, 'common/form.html', {'form': form, 'model': 'branch'})


def upload_branch_pincode(request):
    if request.method == "POST":
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = handle_uploaded_file(request.FILES['file'], request.FILES['file'].name,
                                        MEDIA_ROOT + 'uploads/internal/')
            upload_branch_pincode_file(file)
            return HttpResponseRedirect('/internal/branch')
    else:
        form = ExcelUploadForm()
    return render(request, 'common/upload_form.html', {'form': form})


def branch_pincode(request, branch_id):
    table = BranchPincodeTable(Branch_Pincode.objects.filter(branch_id=branch_id))
    RequestConfig(request, paginate={"per_page": 10}).configure(table)
    return render(request, 'common/table.html', {'table': table, 'model': 'branch pincode'})


def employee(request):
    table = EmployeeTable(Employee.objects.all())
    RequestConfig(request, paginate={"per_page": 10}).configure(table)
    return render(request, 'common/table.html', {'table': table, 'model': 'employee', 'url': 'employee/add'})


def add_employee(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST, instance=Employee())
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/internal/employee')
    else:
        form = EmployeeForm()
    return render(request, 'common/form.html', {'form': form, 'model': 'employee'})


def vehicle(request):
    table = VehicleTable(Vehicle.objects.all())
    RequestConfig(request, paginate={"per_page": 10}).configure(table)
    return render(request, 'internal/vehicle.html', {'table': table})


def add_vehicle(request):
    if request.method == "POST":
        form = VehicleForm(request.POST, instance=Vehicle())
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/internal/vehicle')
    else:
        form = VehicleForm()
    return render(request, 'internal/addvehicle.html', {'form': form})


def upload_vehicle_list(request):
    if request.method == "POST":
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = handle_uploaded_file(request.FILES['file'], request.FILES['file'].name,
                                        MEDIA_ROOT + 'uploads/internal/')
            upload_vehicle_list_file(file)
            return HttpResponseRedirect('/internal/vehicle')
    else:
        form = ExcelUploadForm()
    return render(request, 'common/upload_form.html', {'form': form})


def add_branch_pincode(request):
    if request.method == "POST":
        form = BranchPincodeForm(request.POST, instance=Branch_Pincode())
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/internal/branch_pincode')
    else:
        form = BranchPincodeForm()
    return render(request, 'internal/add_branch_pincode.html', {'form': form})


def branch_get_all(request):
    if request.method == 'POST' and request.is_ajax():
        if 'branch' in request.session:
            form = BranchDropDownForm(initial={'branch': request.session['branch']})
        else:
            form = BranchDropDownForm(initial={'branch': Branch.objects.get(branch_name='HQ').pk})
        return render(request, 'common/dropdown.html', {'form': form})


def branch_get_cash(request):
    if request.is_ajax():
        if 'branch' in request.session:
            cash = Branch.objects.get(pk=request.session['branch']).get_cash(request.GET['type'])
        else:
            cash = sum([branch.get_cash(request.GET['type']) for branch in Branch.objects.exclude(pk=1)])
        return HttpResponse(re.sub('\.[0]*$', '', str(cash)))