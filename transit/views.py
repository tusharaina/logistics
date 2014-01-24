import os
import json
from datetime import datetime
from time import gmtime, strftime

from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table
from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import User
from django_tables2 import RequestConfig
from django.contrib.auth.decorators import login_required
from django.core import serializers

from internal.models import Branch, Vehicle
from .models import TB, TB_History, MTS, DRS, DTO, close_drs
from .forms import CreateMTSForm, CreateTBForm, CreateDRSForm, CreateDTOForm, CreateRTOForm
from awb.models import AWB, AWB_History, AWB_Status
from .tables import TBTable, DRSTable, MTSTable, DTOTable, MTSOutgoingTable
from awb.tables import AWBTable
from utils import generateId


@login_required(login_url='/login')
def tb_incoming(request):
    if 'branch' in request.session:
        table = TBTable(
            TB.objects.filter(delivery_branch=request.session['branch']).exclude(tb_history__mts__status='D'))
    else:
        table = TBTable(TB.objects.exclude(tb_history__mts__status='D'))
    RequestConfig(request, paginate={"per_page": 10}).configure(table)
    return render(request, 'common/table.html',
                  {'table': table, 'url': '/transit/tb/create', 'model': 'tb', 'type': 'incoming'})


def tb_outgoing(request):
    if 'branch' in request.session:
        table = TBTable(
            TB.objects.filter(origin_branch=request.session['branch']).exclude(tb_history__mts__status='D'))
    else:
        table = TBTable(TB.objects.exclude(tb_history__mts__status='D'))
    RequestConfig(request, paginate={"per_page": 10}).configure(table)
    return render(request, 'common/table.html',
                  {'table': table, 'url': '/transit/tb/create', 'model': 'tb', 'type': 'outgoing'})


def show_tb_form(request):
    form = CreateTBForm()
    return render(request, 'transit/create_tb.html', {'form': form, 'model': 'tb'})


def ajax_in_scanning_awb(request):
    if request.method == 'POST' and request.is_ajax():
        request.session['message'] = {}
        try:
            awb = AWB.objects.get(awb=request.POST['awb'])
            awb.readable_status = awb.awb_status.get_readable_choice()
            if awb.awb_status.status in ['ISC', 'PC'] and awb.awb_status.current_branch_id == request.session['branch'] \
                and awb.get_delivery_branch().pk == int(request.POST['delivery_branch']):
                awb.readable_category = awb.awb_status.manifest.get_readable_choice()
                request.session['message']['class'] = 'success'
                request.session['message']['report'] = "AWB: " + str(awb.awb) + " - " + awb.readable_status
                return render(request, 'awb/awb_in_scanning.html', {'awb': awb})
            else:
                request.session['message']['class'] = 'error'
                request.session['message']['report'] = "AWB: " + str(awb.awb) + "  - " + awb.readable_status + \
                                                       " - Delivery Branch: " + awb.get_delivery_branch().branch_name
                return render(request, 'awb/awb_in_scanning.html')
        except AWB.DoesNotExist:
            request.session['message']['class'] = 'error'
            request.session['message']['report'] = "AWB : " + request.POST['awb'] + "  Does not exists"
        return render(request, 'awb/awb_in_scanning.html')


def ajax_get_tb_awbs(request):
    if request.method == "POST" and request.is_ajax():
        fl = AWB.objects.filter(category__in=['COD', 'PRE'],
                                pincode__branch_pincode__branch=request.POST['delivery_branch'],
                                awb_status__current_branch=request.session['branch'],
                                awb_status__status__in=['ISC'])
        rl = AWB.objects.filter(category='REV',
                                awb_status__manifest__branch_id=request.POST['delivery_branch'],
                                awb_status__current_branch=request.session['branch'],
                                awb_status__status__in=['ISC', 'PC'])
        #rto = get_rto_awbs(request.POST['delivery_branch'], request.session['branch'])
        return render(request, 'transit/tb_awb_table.html', {'fl': fl, 'rl': rl})


def reports(request, type='generic'):
    if not request.GET.keys():
        category = zip(*AWB.AWB_TYPE)[1]
        branches = Branch.objects.all()
        awb_status = zip(*AWB_Status.STATUS)[1]
        if type == 'generic':
            return render(request, 'report_generic_input.html',
                          {'category': category, 'branches': branches, 'awb_status': awb_status})
        if type == 'cash-report':
            return render(request, 'report_cash_input.html', {'branches': branches})
    else:
        branch = Branch.objects.all()[0] #todo change to request.user.branch
        awbs = AWB.objects.none()
        if type == 'generic':
            category = 'COD'
            status_type = 'ISC'

            if request.GET.get('category'):
                type_dict = dict(AWB.AWB_TYPE)
                type_dict = {v: k for k, v in type_dict.items()}
                type_of_awbs = type_dict[request.GET.get('category')]

            if request.GET.get('awb_status'):
                status_dict = dict(AWB_Status.STATUS)
                status_dict = {v: k for k, v in status_dict.items()}
                status_type = status_dict[request.GET.get('awb_status')]

            if request.GET.get('branch'):
                branch = Branch.objects.get(pk=int(request.GET.get('branch')))
            print status_type
            awbs = AWB.objects.filter(awb_status__current_tb__tb_history__branch=branch,
                                      category=category,
                                      awb_status__status=status_type)
            #awbs = AWB.objects.all() #todo remove
        elif type == 'cash-report':
            start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            end = datetime.now().replace(microsecond=0)
            if request.GET.get('branch'):
                branch = Branch.objects.get(pk=int(request.GET.get('branch')))

            if request.GET.get('start'):
                start = datetime.strptime(request.GET.get('start'), '%Y-%m-%d')

            if request.GET.get('end'):
                end = datetime.strptime(request.GET.get('end'), '%Y-%m-%d')
            awbs = AWB.objects.filter(on_update__gte=start, on_update__lte=end,
                                      awb_status__current_branch=branch)#todo remove

        doc = SimpleDocTemplate("awbs.pdf", pagesize=(31 * inch, 35 * inch))
        # container for the 'Flowable' objects
        elements = []
        fields = AWB._meta.get_all_field_names()
        fields.remove('awb_status')#todo later add function in models
        fields.remove('awb_history')
        fields.remove('creation_date')
        fields.remove('on_update')
        fields.remove('is_active')
        fields.remove('id')
        awbs = awbs.values_list(*fields)
        data = [fields]
        for awb in awbs:
            data.append(list(awb))
        print data
        t = Table(data)
        elements.append(t)
        # write the document to disk
        doc.build(elements)
        pdf_file = open(doc.filename, 'rb+')
        response = HttpResponse(doc, content_type='application/pdf')
        #response['Content-Disposition'] = 'attachment; filename="awbs.pdf"'
        response.write(pdf_file.read())
        pdf_file.close()

        os.remove(doc.filename)
        return response


def ajax_create_tb(request):
    if request.method == "POST" and request.is_ajax():
        tb = TB(
            tb_id=generateId(TB, request.session['branch'], request.POST['delivery_branch']),
            origin_branch=Branch.objects.get(pk=request.session['branch']),
            delivery_branch=Branch.objects.get(pk=request.POST['delivery_branch']),
            #type=request.POST['type']
        )
        tb.save()
        tb_history = TB_History(
            tb=tb,
            branch=Branch.objects.get(pk=request.session['branch'])
        )
        tb_history.save()
        awbs = json.loads(request.POST['awbs'])
        for awb in awbs:
            awb_status = AWB_Status.objects.get(awb=int(awb))
            if awb_status.status == 'CAN' and awb_status.manifest.category == 'FL':
                AWB_Status.objects.filter(awb=int(awb)).update(current_tb=tb, status='ITR')
                awb_history = AWB_History(
                    awb=AWB.objects.get(pk=int(awb)),
                    tb=tb
                )
                awb_history.save()
            else:
                AWB_Status.objects.filter(awb=int(awb)).update(current_tb=tb, status='TB')
                awb_history = AWB_History(
                    awb=AWB.objects.get(pk=int(awb)),
                    tb=tb
                )
                awb_history.save()
        return HttpResponse(True)
    else:
        return HttpResponse(False)


def mts_incoming(request):
    if 'branch' in request.session:
        table = MTSTable(MTS.objects.filter(to_branch=request.session['branch']).exclude(status='D'))
    else:
        table = MTSTable(MTS.objects.exclude(status='D'))
    RequestConfig(request, paginate={"per_page": 10}).configure(table)
    return render(request, 'common/table.html',
                  {'table': table, 'url': '/transit/mts/create', 'model': 'mts', 'type': 'incoming'})


def mts_outgoing(request):
    if 'branch' in request.session:
        table = MTSOutgoingTable(MTS.objects.filter(from_branch=request.session['branch']).exclude(status='D'))
    else:
        table = MTSOutgoingTable(MTS.objects.exclude(status='D'))
    RequestConfig(request, paginate={"per_page": 10}).configure(table)
    return render(request, 'common/table.html',
                  {'table': table, 'url': '/transit/mts/create', 'model': 'mts', 'type': 'outgoing'})


def show_mts_form(request):
    form = CreateMTSForm()
    return render(request, 'common/form.html', {'form': form, 'model': 'mts'})


def ajax_get_tbs(request):
    if request.method == "POST" and request.is_ajax():
        if 'branch' in request.session:
            tbs = TB.objects.filter(tb_history__branch_id=int(request.session['branch'])).exclude(
                tb_history__mts__from_branch_id=request.session['branch'])
            tblist = [tb for tb in tbs if tb.get_current_branch().pk != tb.delivery_branch.pk]
        else:
            return HttpResponse('Please Select Branch')
        if len(tblist) > 0:
            return render(request, 'transit/ajax_get_tbs.html', {'tbs': tblist})
        else:
            return HttpResponse('No TB available for delivery')


def ajax_create_mts(request):
    if request.method == "POST" and request.is_ajax():
        mts = MTS(
            mts_id=generateId(MTS, request.session['branch'], request.POST['to_branch']),
            from_branch=Branch.objects.get(pk=int(request.session['branch'])),
            to_branch=Branch.objects.get(pk=int(request.POST['to_branch'])),
            type=str(request.POST['type'])
        )
        mts.save()
        tbs = json.loads(request.POST['tbs'])
        for tb in tbs:
            tb_history = TB_History(
                tb=TB.objects.get(pk=int(tb)),
                mts=mts
            )
            tb_history.save()
            awb_status = AWB_Status.objects.filter(current_tb_id=int(tb), status__in=['TB', 'TBD', 'MTS', 'MTD'])
            awb_status.update(current_mts=mts, status='MTS')
            for status in awb_status:
                awb_history = AWB_History(
                    awb=status.awb,
                    mts=mts
                )
                awb_history.save()
        return HttpResponse(True)
    else:
        return HttpResponse(False)


def drs(request):
    if 'branch' in request.session:
        table = DRSTable(DRS.objects.filter(branch=request.session['branch']).exclude(status='C'))
    else:
        table = DRSTable(DRS.objects.exclude(status='C'))
    RequestConfig(request, paginate={"per_page": 10}).configure(table)
    return render(request, 'common/table.html', {'table': table, 'url': 'drs/create', 'model': 'drs', 'type': 'open'})


def ajax_get_drs_awbs(request):
    if request.method == "GET" and request.is_ajax():
        if 'branch' in request.session:
            fl = AWB.objects.filter(awb_status__status__in=['DCR', 'CAN', 'DBC', 'CNA', 'SCH'],
                                    pincode__branch_pincode__branch_id=request.session['branch']).exclude(
                category='REV').order_by(request.GET['sort'])
            rl = AWB.objects.filter(awb_status__status__in=['DR', 'DBC', 'CNA', 'SCH'], category='REV',
                                    pincode__branch_pincode__branch_id=request.session['branch']).order_by(
                request.GET['sort'])
        else:
            fl = AWB.objects.filter(awb_status__status__in=['DCR', 'CAN', 'DBC', 'CNA', 'SCH']).exclude(
                category='REV').order_by(request.GET['sort'])
            rl = AWB.objects.filter(awb_status__status__in=['DR', 'DBC', 'CNA', 'SCH'], category='REV').order_by(
                request.GET['sort'])
        return render(request, 'transit/drs_awb_table.html', {'fl': fl, 'rl': rl})


def ajax_get_dto_awbs(request):
    if request.method == "POST" and request.is_ajax():
        if 'branch' in request.session:
            rl = AWB.objects.filter(awb_status__status__in=['DCR', 'CB', 'RBC'], category='REV',
                                    awb_status__manifest__branch_id=request.session['branch'])
            # fl = AWB.objects.filter(awb_status__status='CAN',s
            #                         pincode__branch_pincode__branch_id=request.session['branch']).exclude(
            #     category='REV')
        else:
            rl = AWB.objects.filter(awb_status__status__in=['DCR', 'CB', 'RBC'], category='REV')
            # fl = AWB.objects.filter(awb_status__status='CAN').exclude(category='REV')
        return render(request, 'transit/dto_awb_table.html', {'rl': rl})

def ajax_get_rto_awbs(request):
    if request.method == "POST" and request.is_ajax():
        if 'branch' in request.session:
            rl = AWB.objects.filter(awb_status__status__in=['CAN', 'RET'],
                                    awb_status__manifest__branch_id=request.session['branch']).exclude(category='REV')
            # fl = AWB.objects.filter(awb_status__status='CAN',s
            #                         pincode__branch_pincode__branch_id=request.session['branch']).exclude(
            #     category='REV')
        else:
            rl = AWB.objects.filter(awb_status__status__in=['CAN', 'RET']).exclude(category='REV')
            # fl = AWB.objects.filter(awb_status__status='CAN').exclude(category='REV')
        return render(request, 'transit/rto_awb_table.html', {'rl': rl})


def ajax_create_drs(request):
    if request.method == "POST" and request.is_ajax():
        if 'branch' not in request.session:
            return HttpResponse('Please select Branch')
        drs = DRS(
            drs_id=generateId(DRS, request.session['branch']),
            fe=User.objects.get(pk=int(request.POST['fe'])),
            vehicle=Vehicle.objects.get(pk=int(request.POST['vehicle'])),
            opening_km=request.POST['opening_km'],
            branch=Branch.objects.get(pk=int(request.session['branch']))
        )
        drs.save()
        fl = list(set(json.loads(request.POST['fl'])))
        rl = list(set(json.loads(request.POST['rl'])))
        for awb in fl:
            awb_obj = AWB.objects.get(pk=int(awb))
            if awb_obj.category == 'REV':
                AWB_Status.objects.filter(awb=int(awb)).update(current_drs=drs, status='PP')
            else:
                AWB_Status.objects.filter(awb=int(awb)).update(current_drs=drs, status='DRS')
            awb_history = AWB_History(
                awb=AWB.objects.get(pk=int(awb)),
                drs=drs
            )
            awb_history.save()

        for awb in rl:
            AWB_Status.objects.filter(awb=int(awb)).update(current_drs=drs, status='PP')
            awb_history = AWB_History(
                awb=AWB.objects.get(pk=int(awb)),
                drs=drs
            )
            awb_history.save()
        return HttpResponse(True)
    else:
        return HttpResponse(False)


def tb_detail(request, tb_id):
    table = AWBTable(AWB.objects.filter(awb_status__current_tb=tb_id))
    RequestConfig(request, paginate={"per_page": 10}).configure(table)
    return render(request, 'common/table.html', {'table': table})


def mts_detail(request, mts_id):
    table = TBTable(TB.objects.filter(tb_history__mts=mts_id))
    RequestConfig(request, paginate={"per_page": 10}).configure(table)
    return render(request, 'common/table.html', {'table': table})


def mts_update_status(request):
    if request.method == 'POST' and request.is_ajax():
        mts = MTS.objects.filter(mts_id=request.POST['mts_id'])
        mts.update(status=request.POST['status'])
        if mts[0].status == 'D':
            tbs = mts[0].get_tbs()
            for tb in tbs:
                tb_history = TB_History(tb_id=tb.tb_id, branch=mts[0].to_branch)
                tb_history.save()
                AWB_Status.objects.filter(current_tb=tb).update(current_branch=mts[0].to_branch)
        return HttpResponse(mts[0].get_readable_choice())


def drs_update_status(request):
    if request.method == 'POST' and request.is_ajax():
        drs = DRS.objects.filter(pk=int(request.POST['drs_id']))
        drs.update(status=request.POST['status'])
        return HttpResponse(drs[0].get_readable_choice())


def drs_detail(request, drs_id):
    data=serializers.serialize('json',DRS.objects.all())#(id=int(drs_id)))
    return HttpResponse(data,mimetype='application/json')

    # fl = AWB.objects.filter(awb_status__current_drs=drs_id).exclude(category='REV').order_by('category')
    # rl = AWB.objects.filter(awb_status__current_drs=drs_id, category='REV').order_by('category')
    # return render(request, 'transit/awb_status_update.html',
    #               {'fl': fl, 'rl': rl, 'drs': DRS.objects.get(pk=drs_id), 'model': 'drs'})


def dto_detail(request, dto_id):
    rl = AWB.objects.filter(awb_status__current_dto=dto_id)
    return render(request, 'transit/awb_status_update.html',
                  {'rl': rl, 'id': DTO.objects.get(pk=dto_id).dto_id, 'model': 'dto'}).order_by('awb')


def drs_in_scanning(request):
    if request.method == 'POST' and request.is_ajax():
        request.session['message'] = {}
        try:
            awb = AWB.objects.get(awb=request.POST['awb'])
            if awb.awb_status.manifest.category == 'FL':
                if awb.get_delivery_branch().pk == request.session['branch']:
                    if awb.awb_status.status in ['DCR', 'CAN', 'SCH', 'DBC', 'CNA']:
                        request.session['message']['class'] = 'success'
                        request.session['message']['report'] = "AWB: " + str(awb.awb) + " | Status: " + str(
                            awb.awb_status.get_readable_choice())
                        return render(request, 'awb/awb_in_scanning.html', {'awb': awb})
                    else:
                        request.session['message']['class'] = 'error'
                        request.session['message']['report'] = "AWB: " + str(awb.awb) + " | Status: " + str(
                            awb.awb_status.get_readable_choice())
                        return HttpResponse('')
                else:
                    request.session['message']['class'] = 'error'
                    request.session['message']['report'] = "AWB: " + str(awb.awb) + " | Status: " + str(
                        awb.awb_status.get_readable_choice()) + " | Delivery Branch: " + str(
                        awb.get_delivery_branch().branch_name)
                    return HttpResponse('')
            else:
                if awb.awb_status.status in ['DR', 'CAN', 'SCH', 'DBC', 'CB', 'CNA']:
                    request.session['message']['class'] = 'success'
                    request.session['message']['report'] = "AWB: " + str(awb.awb) + " | Status: " + str(
                        awb.awb_status.get_readable_choice())
                    return render(request, 'awb/awb_in_scanning.html', {'awb': awb})
                else:
                    request.session['message']['class'] = 'error'
                    request.session['message']['report'] = "AWB: " + str(awb.awb) + " | Status: " + str(
                        awb.awb_status.get_readable_choice())
                    return HttpResponse('')
        except AWB.DoesNotExist:
            request.session['message']['class'] = 'error'
            request.session['message']['report'] = "   AWB: " + request.POST['awb'] + " | Status: Does Not Exists"
            return HttpResponse('')
    else:
        form = CreateDRSForm()
        if 'branch' in request.session:
            form.fields['fe'].queryset = User.objects.filter(profile__branch_id=request.session['branch'],
                                                             profile__role='FE')
            form.fields['vehicle'].queryset = Vehicle.objects.filter(branch_id=request.session['branch'])
        return render(request, 'transit/drs_creation_form.html', {'form': form, 'model': 'drs'})


def drs_get_print_sheet(request):
    data = list(set(json.loads(request.GET['awbs'])))
    awbs = AWB.objects.filter(pk__in=data).order_by('category')
    drs = awbs[0].awb_status.current_drs
    #print user.branch.branch_name
    context = {
        'drs': drs,
        'awbs': awbs,
        'CODs': len([awb for awb in awbs if awb.category == 'COD']),
        'PREs': len([awb for awb in awbs if awb.category == 'PRE']),
        'REVs': len([awb for awb in awbs if awb.category == 'REV']),
        #'branch': Branch.objects.get(pk=int(request.session['branch'])).branch_name,
        'datetime': strftime("%Y-%m-%d %H:%M", gmtime())
    }
    return render(request, 'transit/drs_print_sheet.html', context)


def drs_get_cash(request):
    if request.is_ajax():
        drs = DRS.objects.get(drs_id=request.GET['drs'])
        if request.GET['type'] == 'total':
            return HttpResponse(drs.get_expected_amount())
        else:
            return HttpResponse(drs.get_collected_amount())


def dto_get_print_sheet(request):
    data = list(set(json.loads(request.GET['awbs'])))
    awbs = []
    #print data
    for awb in data:
        awbs.append(AWB.objects.get(pk=int(awb)))
        #user = request.user.get_profile()
    dto = awbs[0].awb_status.current_dto
    #print user.branch.branch_name
    context = {
        'dto': dto,
        'awbs': awbs,
        'client': awbs[0].awb_status.manifest.client.client_name,
        #'branch': Branch.objects.get(pk=int(request.session['branch'])).branch_name,
        'datetime': strftime("%Y-%m-%d %H:%M", gmtime())
    }
    return render(request, 'transit/dto_print_sheet.html', context)


def dto(request):
    if 'branch' in request.session:
        table = DTOTable(DTO.objects.filter(branch=request.session['branch']).exclude(status='C'))
    else:
        table = DTOTable(DTO.objects.exclude(status='C'))
    RequestConfig(request, paginate={"per_page": 10}).configure(table)
    return render(request, 'common/table.html', {'table': table, 'url': 'dto/create', 'model': 'dto', 'type': 'open'})


def dto_in_scanning(request):
    if request.method == 'POST' and request.is_ajax():
        request.session['message'] = {}
        try:
            awb = AWB.objects.get(awb=request.POST['awb'])
            if awb.awb_status.manifest.category == 'RL':
                if awb.get_delivery_branch().pk == request.session['branch']:
                    if awb.awb_status.status in ['DCR', 'CAN', 'RBC', 'CB']:
                        request.session['message']['class'] = 'success'
                        request.session['message']['report'] = "AWB: " + str(awb.awb) + " | Status: " + str(
                            awb.awb_status.get_readable_choice())
                        return render(request, 'transit/dto_in_scanning.html', {'awb': awb})
                    else:
                        request.session['message']['class'] = 'error'
                        request.session['message']['report'] = "AWB: " + str(awb.awb) + " | Status: " + str(
                            awb.awb_status.get_readable_choice())
                        return HttpResponse('')
                else:
                    request.session['message']['class'] = 'error'
                    request.session['message']['report'] = "AWB: " + str(awb.awb) + " | Status: " + str(
                        awb.awb_status.get_readable_choice()) + " | Delivery Branch: " + str(
                        awb.get_delivery_branch().branch_name)
                    return HttpResponse('')
            else:
                if awb.get_delivery_branch().pk == request.session['branch']:
                    if awb.awb_status.status in ['CAN', 'ITR']:
                        request.session['message']['class'] = 'error'
                        request.session['message']['report'] = "AWB: " + str(awb.awb) + " | Status: " + str(
                            awb.awb_status.get_readable_choice())
                        return HttpResponse('')
                    else:
                        request.session['message']['class'] = 'error'
                        request.session['message']['report'] = "AWB: " + str(awb.awb) + " | Status: " + str(
                            awb.awb_status.get_readable_choice())
                        return HttpResponse('')
                else:
                    request.session['message']['class'] = 'error'
                    request.session['message']['report'] = "AWB: " + str(awb.awb) + " | Status: " + str(
                        awb.awb_status.get_readable_choice())
                    return HttpResponse('')
        except AWB.DoesNotExist:
            request.session['message']['class'] = 'error'
            request.session['message']['report'] = "AWB: " + request.POST['awb'] + " | Status: Does Not Exists"
            return HttpResponse('')
    else:
        form = CreateDTOForm()
        if 'branch' in request.session:
            form.fields['fe'].queryset = User.objects.filter(profile__branch_id=request.session['branch'],
                                                             profile__role='FE')
            form.fields['vehicle'].queryset = Vehicle.objects.filter(branch_id=request.session['branch'])
        return render(request, 'transit/dto_creation_form.html', {'form': form, 'model': 'dto'})

def rto_in_scanning(request):
    if request.method == 'POST' and request.is_ajax():
        request.session['message'] = {}
        try:
            awb = AWB.objects.get(awb=request.POST['awb'])
            if awb.awb_status.manifest.category == 'RL':
                if awb.get_delivery_branch().pk == request.session['branch']:
                    if awb.awb_status.status in ['DCR', 'CAN', 'RBC', 'CB']:
                        request.session['message']['class'] = 'success'
                        request.session['message']['report'] = "AWB: " + str(awb.awb) + " | Status: " + str(
                            awb.awb_status.get_readable_choice())
                        return render(request, 'transit/dto_in_scanning.html', {'awb': awb})
                    else:
                        request.session['message']['class'] = 'error'
                        request.session['message']['report'] = "AWB: " + str(awb.awb) + " | Status: " + str(
                            awb.awb_status.get_readable_choice())
                        return HttpResponse('')
                else:
                    request.session['message']['class'] = 'error'
                    request.session['message']['report'] = "AWB: " + str(awb.awb) + " | Status: " + str(
                        awb.awb_status.get_readable_choice()) + " | Delivery Branch: " + str(
                        awb.get_delivery_branch().branch_name)
                    return HttpResponse('')
            else:
                if awb.get_delivery_branch().pk == request.session['branch']:
                    if awb.awb_status.status in ['CAN', 'ITR']:
                        request.session['message']['class'] = 'error'
                        request.session['message']['report'] = "AWB: " + str(awb.awb) + " | Status: " + str(
                            awb.awb_status.get_readable_choice())
                        return HttpResponse('')
                    else:
                        request.session['message']['class'] = 'error'
                        request.session['message']['report'] = "AWB: " + str(awb.awb) + " | Status: " + str(
                            awb.awb_status.get_readable_choice())
                        return HttpResponse('')
                else:
                    request.session['message']['class'] = 'error'
                    request.session['message']['report'] = "AWB: " + str(awb.awb) + " | Status: " + str(
                        awb.awb_status.get_readable_choice())
                    return HttpResponse('')
        except AWB.DoesNotExist:
            request.session['message']['class'] = 'error'
            request.session['message']['report'] = "AWB: " + request.POST['awb'] + " | Status: Does Not Exists"
            return HttpResponse('')
    else:
        form = CreateRTOForm()
        if 'branch' in request.session:
            form.fields['fe'].queryset = User.objects.filter(profile__branch_id=request.session['branch'],
                                                             profile__role='FE')
            form.fields['vehicle'].queryset = Vehicle.objects.filter(branch_id=request.session['branch'])
        return render(request, 'transit/rto_creation_form.html', {'form': form, 'model': 'rto'})


def ajax_create_dto(request):
    if request.method == "POST" and request.is_ajax():
        dto = DTO(
            dto_id=generateId(DTO, request.session['branch']),
            fe=User.objects.get(pk=int(request.POST['fe'])),
            vehicle=Vehicle.objects.get(pk=int(request.POST['vehicle'])),
            branch=Branch.objects.get(pk=int(request.session['branch']))
        )
        dto.save()
        awbs = list(set(json.loads(request.POST['awbs'])))
        for awb in awbs:
            if AWB_Status.objects.get(awb=int(awb)).manifest.category == 'RL':
                AWB_Status.objects.filter(awb=int(awb)).update(current_dto=dto,
                                                               status='DTO')
                awb_history = AWB_History(
                    awb=AWB.objects.get(pk=int(awb)),
                    dto=dto
                )
                awb_history.save()
                # else:
                #     AWB_Status.objects.filter(awb=int(awb), status__in=['CAN', 'ITR']).update(current_dto=dto,
                #                                                                               status='DPR')
                #     awb_history = AWB_History(
                #         awb=AWB.objects.get(pk=int(awb)),
                #         dto=dto
                #     )
                #     awb_history.save()
        return HttpResponse(True)
    else:
        return HttpResponse(False)


def drs_awb_cancel_scan(request):
    if request.method == 'POST' and request.is_ajax():
        request.session['message'] = {}
        awb = AWB.objects.get(awb=str(request.POST['awb']))
        if awb.pk == int(request.POST['id']):
            if awb.category == 'REV':
                if awb.get_delivery_branch().pk == request.session['branch']:
                    AWB_Status.objects.filter(awb=awb.pk).update(status='DCR', current_branch=request.session['branch'],
                                                                 updated_by=request.user)
                    AWB_History.objects.create(awb=awb, status='DCR', branch_id=request.session['branch'])
                else:
                    AWB_Status.objects.filter(awb=awb.pk).update(status='PC', current_branch=request.session['branch'],
                                                                 updated_by=request.user)
                    AWB_History.objects.create(awb=awb, status='PC', branch_id=request.session['branch'])
                request.session['message']['class'] = 'success'
                request.session['message']['report'] = "AWB: " + str(awb.awb) + " | Status: Pick-up Completed" + \
                                                       " | DTO Branch: " + \
                                                       str(awb.get_delivery_branch().branch_name)
                close_drs(awb.awb_status.current_drs.pk)
                return HttpResponse('PC')
            else:
                AWB_Status.objects.filter(awb=awb.pk).update(status=request.POST['status'],
                                                             current_branch=request.session['branch'],
                                                             updated_by=request.user)
                AWB_History.objects.create(awb=awb, status=request.POST['status'], branch_id=request.session['branch'])
                request.session['message']['class'] = 'success'
                request.session['message']['report'] = "AWB: " + str(
                    awb.awb) + " | Status: " + awb.awb_status.get_readable_choice()
                close_drs(awb.awb_status.current_drs.pk)
                return HttpResponse('DCR')
        else:
            request.session['message']['class'] = 'error'
            request.session['message']['report'] = "AWB: " + str(awb.awb) + " | Status: " + str(
                awb.awb_status.get_readable_choice())
            close_drs(awb.awb_status.current_drs.pk)
            return HttpResponse('')


def drs_awb_update_status(request):
    if request.method == 'POST' and request.is_ajax():
        awbs = json.loads(request.POST['awbs'])
        collected_amts = json.loads(request.POST['collected_amts'])
        awbs_dict = dict(zip(awbs, collected_amts))
        for k, v in awbs_dict.items():
            awb = AWB.objects.get(pk=int(k))
            if awb.category == 'REV':
                # if awb.awb_status.status in ['PC', 'DCR']:
                #     AWB_Status.objects.filter(awb=awb).update(status=str(request.POST['awb_status']))
                pass
            else:
                if awb.awb_status.status in ['DRS', 'DCR']:
                    if awb.category == 'COD':
                        AWB_Status.objects.filter(awb=awb).update(status=str(request.POST['awb_status']),
                                                                  updated_by=request.user)
                        AWB_Status.objects.filter(awb=awb).update(collected_amt=str(v))
                    else:
                        AWB_Status.objects.filter(awb=awb).update(status=str(request.POST['awb_status']),
                                                                  updated_by=request.user)
            close_drs(awb.awb_status.current_drs.pk)
        return HttpResponse(True)


def dto_awb_update_status(request):
    if request.method == 'POST' and request.is_ajax():
        awbs = json.loads(request.POST['awbs'])
        for id in awbs:
            awb = AWB.objects.get(pk=int(id))
            if awb.category == 'REV':
                AWB_Status.objects.filter(awb=awb).update(status=str(request.POST['awb_status']),
                                                          updated_by=request.user)
            else:
                AWB_Status.objects.filter(awb=awb).update(status='RET')
            AWB_History.objects.create(awb=awb, branch_id=request.session['branch'], status=request.POST['awb_status'])
            if awb.awb_status.current_dto.get_awb_close_count() == awb.awb_status.current_dto.get_awb_count():
                DTO.objects.filter(pk=awb.awb_status.current_dto.pk).update(status='C')
        return HttpResponse(True)


def drs_awb_status_update(request):
    if request.method == 'POST' and request.is_ajax():
        request.session['message'] = {}
        if 'reason' in request.POST:
            reason = request.POST['reason']
        else:
            reason = ''
        awb = AWB.objects.get(pk=int(request.POST['awb']))
        if awb.category == 'REV':
            AWB_Status.objects.filter(awb=awb.pk).update(status=str(request.POST['status']),
                                                         reason=reason, updated_by=request.user)
        else:
            if awb.category == 'COD':
                if request.POST['coll_amt'] != '':
                    AWB_Status.objects.filter(awb=awb.pk).update(status=str(request.POST['status']),
                                                                 collected_amt=float(request.POST['coll_amt']),
                                                                 reason=reason, updated_by=request.user)
                else:
                    AWB_Status.objects.filter(awb=awb.pk).update(status=str(request.POST['status']),
                                                                 reason=reason, updated_by=request.user)
            else:
                AWB_Status.objects.filter(awb=awb.pk).update(status=str(request.POST['status']),
                                                             reason=reason, updated_by=request.user)
        AWB_History.objects.create(awb=awb, status=str(request.POST['status']), branch_id=request.session['branch'])
        request.session['message']['class'] = 'success'
        request.session['message']['report'] = "AWB: " + str(awb.awb) + " | Status: " + str(
            AWB_Status.objects.get(awb=awb.pk).get_readable_choice())
        close_drs(awb.awb_status.current_drs.pk)
        return HttpResponse(True)


def get_count(request):
    if request.is_ajax():
        if request.GET['model'] == 'awb':
            if request.GET['type'] == 'incoming':
                if 'branch' in request.session:
                    if request.GET['category'] != '':
                        return HttpResponse(
                            AWB.objects.filter(pincode__branch_pincode__branch_id=request.session['branch'],
                                               category=request.GET['category']).exclude(
                                awb_status__status__in=['DEL', 'RET']).count())
                    else:
                        return HttpResponse(
                            AWB.objects.filter(pincode__branch_pincode__branch_id=request.session['branch']).exclude(
                                awb_status__status__in=['DEL', 'RET']).count())
                else:
                    if request.GET['category'] != '':
                        return HttpResponse(AWB.objects.filter(category=request.GET['category']).exclude(
                            awb_status__status__in=['DEL', 'RET']).count())
                    else:
                        return HttpResponse(AWB.objects.exclude(awb_status__status__in=['DEL', 'RET']).count())
            else:
                if 'branch' in request.session:
                    if request.GET['category'] != '':
                        return HttpResponse(
                            AWB.objects.filter(awb_status__current_branch_id=request.session['branch'],
                                               category=request.GET['category']).exclude(
                                awb_status__status__in=['DEL', 'RET']).count())
                    else:
                        return HttpResponse(
                            AWB.objects.filter(awb_status__current_branch_id=request.session['branch']).exclude(
                                awb_status__status__in=['DEL', 'RET']).count())
                else:
                    if request.GET['category'] != '':
                        return HttpResponse(AWB.objects.filter(category=request.GET['category']).exclude(
                            awb_status__status__in=['DEL', 'RET']).count())
                    else:
                        return HttpResponse(AWB.objects.exclude(awb_status__status__in=['DEL', 'RET']).count())
        elif request.GET['model'] == 'tb':
            if request.GET['type'] == 'incoming':
                if 'branch' in request.session:
                    return HttpResponse(TB.objects.filter(delivery_branch_id=request.session['branch']).exclude(
                        tb_history__mts__status='D').count())
                else:
                    return HttpResponse(TB.objects.exclude(tb_history__mts__status='D').count())
            else:
                if 'branch' in request.session:
                    return HttpResponse(TB.objects.filter(origin_branch_id=request.session['branch']).exclude(
                        tb_history__mts__status='D').count())
                else:
                    return HttpResponse(TB.objects.exclude(tb_history__mts__status='D').count())
        elif request.GET['model'] == 'mts':
            if request.GET['type'] == 'incoming':
                if 'branch' in request.session:
                    return HttpResponse(
                        MTS.objects.filter(to_branch_id=request.session['branch']).exclude(status='D').count())
                else:
                    return HttpResponse(MTS.objects.exclude(status='D').count())
            else:
                if 'branch' in request.session:
                    return HttpResponse(
                        MTS.objects.filter(from_branch_id=request.session['branch']).exclude(status='D').count())
                else:
                    return HttpResponse(MTS.objects.exclude(status='D').count())
        elif request.GET['model'] == 'drs':
            if 'branch' in request.session:
                return HttpResponse(DRS.objects.filter(branch_id=request.session['branch']).exclude(status='C').count())
            else:
                return HttpResponse(DRS.objects.exclude(status='C').count())
        elif request.GET['model'] == 'dto':
            if 'branch' in request.session:
                return HttpResponse(DTO.objects.filter(branch_id=request.session['branch']).exclude(status='C').count())
            else:
                return HttpResponse(DTO.objects.exclude(status='C').count())


def drs_update_closing_km(request):
    if request.method == 'GET' and request.is_ajax():
        request.session['message'] = {}
        drs = DRS.objects.get(drs_id=request.GET['drs_id'])
        drs.closing_km = request.GET['closing_km']
        drs.save()
        close_drs(drs.pk)
        request.session['message']['class'] = 'success'
        request.session['message']['report'] = 'DRS : ' + drs.drs_id + ' | Closing Km : ' + request.GET[
            'closing_km'] + ' Km'
    return HttpResponse(True)