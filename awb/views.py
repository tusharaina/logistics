from __future__ import unicode_literals
from time import gmtime, strftime
import json
import csv,time
import re

from django_tables2 import RequestConfig
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
from django.utils.formats import date_format
from django.core import serializers

from awb.serializers import UserSerializer
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from awb.models import AWB
from django.views.decorators.csrf import csrf_exempt

from utils.upload import get_manifest_filename, upload_manifest_data
from utils.constants import AWB_STATUS, AWB_FL_REMARKS, AWB_RL_REMARKS
from .forms import UploadManifestForm
from .tables import AWBTable, ManifestTable, AWBFLTable, AWBRLTable, AWBCODTable, AWBCODTable1
from .models import AWB, Manifest, AWB_Status, AWB_History
from client.models import Client_Warehouse, Client
from internal.models import Branch, Branch_Pincode
from transit.models import TB, MTS


@login_required(login_url='/login')
def awb_incoming(request):
    if 'branch' in request.session:
        fl_tbl = AWBFLTable(AWB.objects.filter(pincode__branch_pincode__branch_id=request.session['branch'],
                                               category__in=['COD', 'PRE']).exclude(
            awb_status__status__in=['DEL', 'RET']))
        rl_tbl = AWBRLTable(
            AWB.objects.filter(pincode__branch_pincode__branch_id=request.session['branch'], category='REV').exclude(
                awb_status__status__in=['DEL', 'RET']))
    else:
        fl_tbl = AWBFLTable(
            AWB.objects.filter(category__in=['COD', 'PRE']).exclude(awb_status__status__in=['DEL', 'RET']))
        rl_tbl = AWBRLTable(AWB.objects.filter(category='REV').exclude(awb_status__status__in=['DEL', 'RET']))
    RequestConfig(request, paginate={"per_page": 10}).configure(fl_tbl)
    RequestConfig(request, paginate={"per_page": 10}).configure(rl_tbl)
    return render(request, 'awb/awb.html', {'fl_tbl': fl_tbl, 'rl_tbl': rl_tbl, 'type': 'incoming'})


def awb_outgoing(request):
    if 'branch' in request.session:
        fl_tbl = AWBFLTable(AWB.objects.filter(awb_status__current_branch_id=request.session['branch'],
                                               category__in=['COD', 'PRE']).exclude(awb_status__status__in=['DEL', 'RET']))
        rl_tbl = AWBRLTable(
            AWB.objects.filter(awb_status__current_branch_id=request.session['branch'], category='REV').exclude(
                awb_status__status__in=['DEL', 'RET']))
    else:
        fl_tbl = AWBFLTable(
            AWB.objects.filter(category__in=['COD', 'PRE']).exclude(awb_status__status__in=['DEL', 'RET']))
        rl_tbl = AWBRLTable(AWB.objects.filter(category='REV').exclude(awb_status__status__in=['DEL', 'RET']))
    RequestConfig(request, paginate={"per_page": 10}).configure(fl_tbl)
    RequestConfig(request, paginate={"per_page": 10}).configure(rl_tbl)
    return render(request, 'awb/awb.html', {'fl_tbl': fl_tbl, 'rl_tbl': rl_tbl, 'type': 'outgoing'})

def awb_cod(request):
    if 'branch' in request.session:
        fl_tbl= AWBFLTable(AWB.objects.filter(awb_status__current_branch_id=request.session['branch'],
                                             category='COD').exclude(awb_status__status__in=['DEL', 'RET']))
    else:
        fl_tbl= AWBFLTable(AWB.objects.filter(category='COD').exclude(awb_status__status__in=['DEL', 'RET']))
    RequestConfig(request, paginate={"per_page": 10}).configure(fl_tbl)
    return render(request, 'awb/awb.html', {'fl_tbl': fl_tbl, 'type': 'cod'})

def awb_prepaid(request):
    if 'branch' in request.session:
        fl_tbl= AWBFLTable(AWB.objects.filter(awb_status__current_branch_id=request.session['branch'],
                                             category='PRE').exclude(awb_status__status__in=['DEL', 'RET']))
    else:
        fl_tbl= AWBFLTable(AWB.objects.filter(category='PRE').exclude(awb_status__status__in=['DEL', 'RET']))
    RequestConfig(request, paginate={"per_page": 10}).configure(fl_tbl)
    return render(request, 'awb/awb.html', {'fl_tbl': fl_tbl, 'type': 'prepaid'})

def awb_reverse(request):
    if 'branch' in request.session:
        fl_tbl= AWBFLTable(AWB.objects.filter(awb_status__current_branch_id=request.session['branch'],
                                             category='REV').exclude(awb_status__status__in=['DEL', 'RET']))
    else:
        fl_tbl= AWBFLTable(AWB.objects.filter(category='REV').exclude(awb_status__status__in=['DEL', 'RET']))
    RequestConfig(request, paginate={"per_page": 10}).configure(fl_tbl)
    return render(request, 'awb/awb.html', {'fl_tbl': fl_tbl, 'type': 'reverse'})


def expected_cod(request):
    if 'branch' in request.session:
        fl_tbl=AWBCODTable(AWB.objects.filter(awb_status__current_drs__branch_id=request.session['branch'],\
                                             awb_status__current_drs__creation_date__startswith =time.strftime("%Y-%m-%d")))
    else:
        fl_tbl = AWBCODTable(AWB.objects.filter(awb_status__current_drs__creation_date__startswith =time.strftime("%Y-%m-%d")))
    RequestConfig(request, paginate={"per_page": 10}).configure(fl_tbl)
    return render(request, 'awb/awb.html', {'fl_tbl': fl_tbl, 'type': 'cod'})

def collected_cod(request):
    if 'branch' in request.session:
        fl_tbl=AWBCODTable1(AWB.objects.filter(awb_status__current_drs__branch_id=request.session['branch'],\
                                             awb_status__current_drs__creation_date__startswith =time.strftime("%Y-%m-%d")))
    else:
        fl_tbl = AWBCODTable1(AWB.objects.filter(awb_status__current_drs__creation_date__startswith =time.strftime("%Y-%m-%d")))
    RequestConfig(request, paginate={"per_page": 10}).configure(fl_tbl)
    return render(request, 'awb/awb.html', {'fl_tbl': fl_tbl, 'type': 'cod'})


def awb_history(request, awb_id):
        awb = AWB.objects.get(pk=int(awb_id))
        return render(request, 'awb/awb_history.html', {'awb_hist': awb.get_awb_history(), 'awb_details': awb})

def awb_history_mobile(request,awb_id):
        data = serializers.serialize('json', AWB.objects.filter(id=int(awb_id)))
        return HttpResponse(data, mimetype='application/json')



def awb_history_external(request, awb_id):
    data = {}
    awb = AWB.objects.get(awb=awb_id)
    data['details'] = serializers.serialize("json", AWB.objects.filter(awb=awb_id))
    data['history'] = awb.get_awb_history(False)
    data['pincode'] = awb.pincode.pincode
    return HttpResponse(json.dumps(data), content_type="application/json")


def awb_generate_mis(request):
    if request.method == 'POST' and request.POST['start_date'] != '' and request.POST['end_date'] != '':
        start_date = request.POST['start_date'] + ' 00:00:00'
        end_date = request.POST['end_date'] + ' 23:59:59'
        if request.POST['client'] != '':
            awbs = AWB.objects.filter(awb_status__manifest__client__client_code=request.POST['client'],
                                      creation_date__range=(start_date, end_date))
        else:
            awbs = AWB.objects.filter(creation_date__range=(start_date, end_date))
        request.session['awb_mis'] = [awb.pk for awb in awbs]
        request.session['start_date'] = request.POST['start_date']
        request.session['end_date'] = request.POST['end_date']
        return render(request, 'awb/awb_generate_mis.html', {'awbs': awbs, 'clients': Client.objects.all()})
    else:
        return render(request, 'awb/awb_generate_mis.html', {'clients': Client.objects.all()})


def awb_download_mis(request):
    if request.method == 'GET' and 'awb_mis' in request.session and 'end_date' in request.session:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="MIS_"' + str(strftime("%Y-%m-%d_%H-%M-%S",
                                                                                       gmtime())) + '".csv"'

        writer = csv.writer(response)
        header = ['AWB', 'Client', 'Order ID', 'Priority', 'Consignee', 'Address', 'Phone', 'Pincode', 'Category',
                  'Amount', 'COD Amount', 'Weight', 'Delivery Branch', 'Pickup Branch', 'Dispatch Count',
                  'First Pending', 'First Dispatch', 'Last Dispatch', 'Last Scan', 'Current Status',
                  'Last Status on ' + request.session['end_date'], 'First Scan Location', 'CS Call Made', 'Remark',
                  'Reason',
                  'Date']
        writer.writerow(header)
        for id in request.session['awb_mis']:
            awb = AWB.objects.get(pk=id)
            writer.writerow(
                [awb.awb, awb.get_client(), awb.order_id, awb.get_priority(), awb.customer_name,
                 awb.get_full_address(),
                 awb.phone_1, awb.pincode.pincode, awb.get_readable_choice(), awb.package_value,
                 awb.expected_amount, awb.weight, awb.get_delivery_branch(), awb.get_pickup_branch(),
                 awb.get_drs_count(), awb.get_first_pending(), awb.get_first_dispatch(), awb.get_last_dispatch(),
                 awb.get_last_scan(), awb.awb_status.get_readable_choice(),
                 awb.get_status_on_date(request.session['end_date']),
                 awb.get_first_scan_branch(), awb.get_last_call_made_time(), awb.awb_status.remark,
                 awb.awb_status.reason, date_format(awb.creation_date, "SHORT_DATETIME_FORMAT")])

        del request.session['awb_mis']
        del request.session['end_date']
        return response
        # result = generate_mis.delay(request.session['awb_mis'], request.session['end_date'])
        # del request.session['awb_mis']
        # del request.session['end_date']
        # return result.get()
    else:
        return HttpResponse('Server Error')


def manifest(request):
    table = ManifestTable(Manifest.objects.filter(status='O'))
    RequestConfig(request, paginate={"per_page": 10}).configure(table)
    return render(request, 'common/table.html',
                  {'table': table, 'model': 'manifest', 'url': '/transit/manifest/upload'})


def upload_manifest_file(request):
    if request.method == 'POST':
        form = UploadManifestForm(request.POST, request.FILES)
        form.warehouse = Client_Warehouse.objects.filter(client_id=request.POST['client'])
        if form.is_valid():
            manifest = form.save(commit=False)
            file = get_manifest_filename(request.POST, request.FILES['file'])
            manifest.file = file
            manifest.uploaded_by = request.user
            pincode = Client_Warehouse.objects.get(pk=int(request.POST['warehouse'])).pincode
            manifest.branch = Branch_Pincode.objects.get(pincode=pincode).branch
            manifest.save()
            awb_uploaded, awb_existing, wrong_awb, wrong_pincode = upload_manifest_data(manifest.pk, request)
            if len(awb_uploaded) > 0:
                messages.success(request, '%s uploaded successfully' % file.split('/')[2])
            else:
                manifest.delete()
                messages.error(request, '%s already uploaded' % file.split('/')[2])
            context = {
                'manifest': file.split('/')[2],
                'awb_uploaded': awb_uploaded,
                'awb_existing': awb_existing,
                'wrong_pincode': wrong_pincode,
                'wrong_awb': wrong_awb
            }
            return render(request, 'awb/upload_manifest.html', context)
    else:
        form = UploadManifestForm()
    return render(request, 'awb/upload_manifest.html', {'form': form})


def awb_in_scanning(request):
    if request.method == 'POST' and request.is_ajax():
        request.session['message'] = {}
        try:
            awb = AWB.objects.get(awb=request.POST['awb'])
            if awb.awb_status.manifest.category in ['FL', 'RL']:
                if awb.awb_status.status in ['DR', 'PC']:
                    if awb.get_delivery_branch().pk == int(request.session['branch']):
                        AWB_Status.objects.filter(awb=awb.pk).update(status='DCR',
                                                                     current_branch=request.session['branch'])
                        AWB_History.objects.create(status='ISC', branch_id=int(request.session['branch']), awb=awb)
                        AWB_History.objects.create(status='DCR', branch_id=int(request.session['branch']), awb=awb)
                        awb.readable_status = AWB_Status.objects.get(awb=awb).get_readable_choice()
                    else:
                        AWB_Status.objects.filter(awb=awb.pk).update(status='ISC',
                                                                     current_branch=request.session['branch'])
                        AWB_History.objects.create(status='ISC', branch_id=int(request.session['branch']), awb=awb)
                        awb.readable_status = 'In-Scanned'
                    awb.readable_category = awb.awb_status.manifest.get_readable_choice()
                    manifest = awb.awb_status.manifest
                    if manifest.get_expected_awb_count() == manifest.get_in_scanned_awb_count():
                        manifest.status = 'I'
                    request.session['message']['class'] = 'success'
                    request.session['message']['report'] = "AWB : " + str(awb.awb) + " - " + str(awb.readable_status)
                elif awb.awb_status.status in ['TB', 'TBD', 'MTS', 'MTD']:
                    if awb.get_delivery_branch().pk == int(request.session['branch']):
                        AWB_Status.objects.filter(awb=awb.pk).update(status='DCR',
                                                                     current_branch=request.session['branch'])
                        AWB_History.objects.create(status='DCR', branch_id=int(request.session['branch']), awb=awb)
                        awb.readable_status = AWB_Status.objects.get(awb=awb).get_readable_choice()
                    else:
                        AWB_Status.objects.filter(awb=awb.pk).update(status='ISC',
                                                                     current_branch=request.session['branch'])
                        AWB_History.objects.create(status='ISC', branch_id=int(request.session['branch']), awb=awb)
                        awb.readable_status = 'In-Scanned'
                    request.session['message']['class'] = 'success'
                    request.session['message']['report'] = "AWB : " + str(awb.awb) + " - " + str(awb.readable_status)
                else:
                    awb.readable_category = awb.awb_status.manifest.get_readable_choice()
                    awb.readable_status = awb.awb_status.get_readable_choice()
                    request.session['message']['class'] = 'error'
                    request.session['message']['report'] = "AWB : " + str(awb.awb) + " - " + awb.readable_status
            else:
                awb.readable_category = awb.awb_status.manifest.get_readable_choice()
                awb.readable_status = awb.awb_status.get_readable_choice()
                request.session['message']['class'] = 'error'
                request.session['message']['report'] = "AWB : " + str(awb.awb) + " - " + \
                                                       awb.awb_status.get_readable_choice() + " | Category : " + \
                                                       str(awb.awb_status.manifest.get_readable_choice())
            return render(request, 'awb/manifest_awb_in_scanning.html', {'awb': awb})
        except AWB.DoesNotExist:
            request.session['message']['class'] = 'error'
            request.session['message']['report'] = "AWB : " + request.POST['awb'] + " - Does not exists"
            return render(request, 'awb/manifest_awb_in_scanning.html')
    else:
        return render(request, 'awb/manifest_in_scanning.html', {'model': 'manifest'})


def manifest_detail(request, mainfest_id):
    table = AWBTable(AWB.objects.filter(awb_status__manifest=mainfest_id))
    RequestConfig(request, paginate={"per_page": 10}).configure(table)
    return render(request, 'common/table.html', {'table': table})


def awb_print_invoice(request):
    if 'branch' in request.session:
        awbs = AWB.objects.filter(pincode__branch_pincode__branch_id=request.session['branch'], category='REV').exclude(
            awb_status__status__in=['DEL', 'RET'])
    else:
        awbs = AWB.objects.filter(category='REV').exclude(awb_status__status__in=['DEL', 'RET'])
    return render(request, 'awb/awb_print_invoice.html', {'awbs': awbs})


def awb_print_invoice_sheet(request):
    data = json.loads(request.GET['awbs'])
    awbs = []
    #print data
    for awb in data:
        awbs.append(AWB.objects.get(pk=int(awb)))
        #user = request.user.get_profile()
    #print user.branch.branch_name
    context = {
        'awbs': awbs,
        #'branch': Branch.objects.get(pk=int(request.session['branch'])).branch_name,
        'datetime': strftime("%Y-%m-%d %H:%M", gmtime())
    }
    return render(request, 'awb/awb_print_invoice_sheet.html', context)


def manifest_invoice_download(request):
    awbs = json.loads(request.POST['awbs'])
    return HttpResponse(awbs)


def search_awb(request, extra=''):
    if extra == 'advanced_search':
        return render(request, 'advance_search.html')
    if request.GET.get('type'):
        awbs = []
        awb_status = AWB_Status.objects.none()
        type_of_awb = request.GET.get('type')
        if type_of_awb == 'branch':

            branch_id = request.GET.get('awb')
            branch = Branch.objects.filter(pk=int(branch_id))
            if branch:
                awb_status = branch[0].awb_status.exclude(status='DEL')

        elif type_of_awb == 'tb':
            tb_id = request.GET.get('awb')
            tb = TB.objects.filter(pk=int(tb_id))
            awb_status = AWB_Status.objects.filter(current_tb__in=tb)

        elif type_of_awb == 'mts':
            mts_id = request.GET.get('awb')
            mts = MTS.objects.filter(pk=int(mts_id))
            awb_status = AWB_Status.objects.filter(current_mts__in=mts)

        for awb_s in awb_status:
            awbs.append(awb_s.awb)
            #elif type_of_awb == 'dto':
            #    dto = request.GET.get('dto_id')
            #    dto = request.GET.get('dto_id')
    else:
        awbs = re.split('[\s,;]+', request.GET.get('awb'))
        awbs = AWB.objects.filter(awb__in=awbs)
        table = AWBTable(awbs)
        RequestConfig(request, paginate={"per_page": 10}).configure(table)
        return render(request, 'common/search_awb_table.html', {'table': table})


def search_awb_external(request, awbs):
    awbs = re.split('[\s,;]+', request.GET.get('awbs'))
    awbs = AWB.objects.filter(awb__in=awbs)
    data = []
    for awb in awbs:
        data.append({'pk': awb.pk, 'awb': awb.awb, 'status': awb.awb_status.get_readable_choice(),
                     'date': date_format(awb.awb_history_set.all().order_by('-creation_date')[0].creation_date,
                                         "SHORT_DATETIME_FORMAT").upper()})
    return HttpResponse(json.dumps(data), 'application/json')


def awb_status_update(request):
    if request.method == 'POST' and request.is_ajax():
        awbs = json.loads(request.POST['awbs'])
        for awb in awbs:
            AWB_Status.objects.filter(awb=int(awb)).update(status=request.POST['awb_status'])
            AWB_History.objects.create(awb=awb.pk, status=request.POST['awb_status'],
                                       branch_id=request.session['branch'])
        return HttpResponse(True)
    else:
        return HttpResponse(False)


def awb_field_update(request):
    if request.method == 'POST' and request.is_ajax():
        request.session['message'] = {}
        awb = AWB.objects.get(pk=request.POST['awb'])
        if request.POST['field'] == 'weight':
            awb.weight = request.POST['val']
        elif request.POST['field'] == 'length':
            awb.length = request.POST['val']
        elif request.POST['field'] == 'breadth':
            awb.breadth = request.POST['val']
        elif request.POST['field'] == 'height':
            awb.height = request.POST['val']
        awb.save()
        request.session['message']['class'] = 'success'
        request.session['message']['report'] = 'AWB : ' + str(awb.awb) + ' | ' + request.POST['field'].upper() + \
                                               ' : ' + request.POST['val'] + ' cm'
        return HttpResponse(True)
    else:
        return HttpResponse('')


def awb_report_cc(request):
    if request.method == 'GET' and request.is_ajax():
        filter = {}
        if request.GET['client'] != '':
            filter['awb_status__manifest__client__client_code'] = request.GET['client']
        if request.GET['status'] != '':
            if request.GET['status'] == 'INT':
                filter['awb_status__status__in'] = ['TB', 'TBD', 'MTS', 'MTD']
            else:
                filter['awb_status__status'] = request.GET['status']
        if request.GET['start_date'] != '' and request.GET['end_date'] != '':
            filter['creation_date__range'] = (
                request.GET['start_date'] + ' 00:00:00', request.GET['end_date'] + ' 23:59:59')
        if request.GET['priority'] != '':
            filter['priority'] = request.GET['priority']
        awbs = AWB.objects.filter(**filter)
        return render(request, 'awb/awb_status_update_cc.html',
                      {'awbs': awbs, 'awb_rl_remarks': AWB_RL_REMARKS, 'awb_fl_remarks': AWB_FL_REMARKS})
    else:
        return render(request, 'awb/awb_report_call_center.html',
                      {'clients': Client.objects.all(), 'status': AWB_STATUS})


def awb_update_by_cc(request):
    if request.method == 'POST' and request.is_ajax():
        request.session['message'] = {}
        awb = AWB_Status.objects.get(awb=int(request.POST['awb']))
        awb.status = request.POST['status']
        awb.remark = request.POST['remark']
        awb.reason = request.POST['reason']
        awb.updated_by = request.user
        awb.save()
        id = AWB.objects.get(pk=request.POST['awb'])
        request.session['message']['class'] = 'success'
        request.session['message']['report'] = 'AWB : ' + id.awb + ' | Status : ' + id.awb_status.get_readable_choice()
        return HttpResponse(True)
    else:
        request.session['message']['class'] = 'error'
        request.session['message']['report'] = 'Could\'nt Updated : Server Error'
        return HttpResponse('')

class JSONResponse(HttpResponse):
     def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
def awb_list(request, pk):
    """
    List all code request, or create a new request.
    """
    if request.method == 'GET':
        snippets = AWB.objects.filter(pk=int(pk))
        serializer = UserSerializer(snippets, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)

