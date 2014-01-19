from __future__ import unicode_literals
import os
import re
from time import gmtime, strftime

import xlrd
import barcode
from barcode.writer import ImageWriter
from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver

from awb.models import AWB_Status, AWB, Manifest
from internal.models import Branch, Branch_Pincode, Employee, Vehicle
from zoning.models import Pincode, City
from utils.constants import MANIFEST_HEADER_DICT
from utils.random import get_manifest_header_dict
from logistics.settings import MEDIA_ROOT
from client.models import Client


def get_manifest_filename(data, file):
    client_code = str(Client.objects.get(pk=data['client']).client_code).upper()
    datetime = strftime("%Y-%m-%d_%H-%M-%S", gmtime())
    ext = '.' + str(file.name.split('.')[-1]).lower()
    filename = client_code + str('_') + data['category'].upper() + str('_') + datetime + ext
    dir = 'uploads/manifest/'
    handle_uploaded_file(file, filename, MEDIA_ROOT + str(dir))
    return dir + filename


def handle_uploaded_file(file, name, dir):
    with open(dir + name, 'wb+') as destination: #for row in range(0,rows):
    #return [[str(worksheet.cell_value(row, col)) for col in range(0,cols)] for row in range(0,rows)]
        for chunk in file.chunks():
            destination.write(chunk)
    return dir + name


def upload_manifest_data(manifest_id, request):
    manifest = Manifest.objects.get(pk=manifest_id)
    workbook = xlrd.open_workbook(MEDIA_ROOT + manifest.file.name)
    worksheet = workbook.sheet_by_index(0)
    rows = worksheet.nrows
    cols = worksheet.ncols

    header = {}
    for col in range(0, cols):
        val = str(worksheet.cell_value(0, col)).lower().strip()
        header.update(get_manifest_header_dict(val, MANIFEST_HEADER_DICT, col))

    client = Client.objects.get(pk=int(request.POST['client'])).client_code
    awb_uploaded = []
    awb_existing = []
    wrong_pincode = {}
    wrong_awb = []
    for row in range(1, rows):
        try:
            awb = AWB.objects.get(awb=str(worksheet.cell_value(row, header['awb'])).strip())
            awb_existing.append(awb)
        except AWB.DoesNotExist:
            awb = str(worksheet.cell_value(row, header['awb'])).strip()
            if awb[:3].upper() == client:
                #and len(awb) == 10 and awb[3:] <= Client.objects.get(client_code=client).awb_assigned_to[3:]:
                try:
                    pincode = Pincode.objects.get(pincode=int(worksheet.cell_value(row, header['pincode'])))

                    bind = {}
                    if request.POST['category'] == 'RL':
                        bind['category'] = 'REV'
                        bind['barcode'] = generate_barcode(awb)
                    else:
                        bind['category'] = ''
                    for key in header.keys():
                        if key == 'pincode':
                            bind[key] = pincode
                        elif key == 'phone_1':
                            bind[key] = re.sub('\.[^.]*$', '', str(worksheet.cell_value(row, header[key])))
                        elif key == 'phone_2':
                            bind[key] = re.sub('\.[^.]*$', '', str(worksheet.cell_value(row, header[key])))
                        elif key == 'order_id':
                            bind[key] = re.sub('\.[^.]*$', '', str(worksheet.cell_value(row, header[key])))
                        elif key == 'category':
                            if bind[key] == '':
                                if worksheet.cell_value(row, header[key]).upper() == 'COD':
                                    bind[key] = 'COD'
                                else:
                                    bind[key] = 'PRE'
                        elif key == 'expected_amount':
                            if worksheet.cell_value(row, header[key]):
                                bind[key] = int(worksheet.cell_value(row, header[key]))
                            else:
                                bind[key] = int(0)
                        elif key == 'priority':
                            if worksheet.cell_value(row, header[key]).lower().strip() == 'high':
                                bind[key] = 'H'
                            if worksheet.cell_value(row, header[key]).lower().strip() == 'low':
                                bind[key] = 'L'
                            else:
                                bind[key] = 'N'
                        elif worksheet.cell_value(row, header[key]):
                            if type(worksheet.cell_value(row, header[key])) is float:
                                bind[key] = float(worksheet.cell_value(row, header[key]))
                            else:
                                bind[key] = worksheet.cell_value(row, header[key]).strip()
                        else:
                            bind[key] = ''

                    awb = AWB(**bind)
                    awb.save()
                    awb_status = AWB_Status(awb=awb, manifest=manifest)
                    awb_status.save()
                    awb_uploaded.append(awb)
                except Pincode.DoesNotExist:
                    pincode = int(worksheet.cell_value(row, header['pincode']))
                    wrong_pincode[pincode] = str(worksheet.cell_value(row, header['awb'])).strip()
            else:
                wrong_awb.append(awb)
    return awb_uploaded, awb_existing, wrong_awb, wrong_pincode


def upload_branch_pincode_file(file):
    workbook = xlrd.open_workbook(file)
    worksheet = workbook.sheet_by_index(0)
    rows = worksheet.nrows
    cols = worksheet.ncols

    header = {}
    for row in range(0, rows):
        if row == 0:
            for col in range(0, cols):
                cell = str(worksheet.cell_value(0, col)).lower().strip()
                if cell == 'pincode':
                    header['pincode'] = col
                if cell == 'branch':
                    header['branch'] = col
        else:
            pincode = Pincode.objects.get(pincode=int(worksheet.cell_value(row, header['pincode'])))
            try:
                branch = Branch.objects.get(branch_name=str(worksheet.cell_value(row, header['branch'])).strip())
                try:
                    Branch_Pincode.objects.get(branch=branch.pk, pincode=pincode.pk)
                except Branch_Pincode.DoesNotExist:
                    branch_pincode = Branch_Pincode(branch_id=branch.pk, pincode_id=pincode.pk)
                    branch_pincode.save()
            except Branch.DoesNotExist:
                branch = Branch(branch_name=str(worksheet.cell_value(row, header['branch'])).strip())
                branch.save()
                try:
                    Branch_Pincode.objects.get(branch=branch.pk, pincode=pincode.pk)
                except Branch_Pincode.DoesNotExist:
                    branch_pincode = Branch_Pincode(
                        branch_id=branch.pk,
                        pincode_id=pincode.pk
                    )
                    branch_pincode.save()


def upload_pincode_city_file(file):
    workbook = xlrd.open_workbook(file)
    worksheet = workbook.sheet_by_index(0)
    rows = worksheet.nrows
    cols = worksheet.ncols

    header = {}
    for row in range(0, rows):
        if row == 0:
            for col in range(0, cols):
                cell = str(worksheet.cell_value(0, col)).lower().strip()
                if cell == 'pincode':
                    header['pincode'] = col
                if cell == 'city':
                    header['city'] = col
                if cell == 'state':
                    header['state'] = col
        else:
            try:
                city = City.objects.get(city=str(worksheet.cell_value(row, header['city'])).strip())
            except City.DoesNotExist:
                city = City(
                    city=str(worksheet.cell_value(row, header['city'])).strip(),
                    state=str(worksheet.cell_value(row, header['state'])).strip()
                )
                city.save()
            try:
                pincode = Pincode.objects.get(pincode=int(worksheet.cell_value(row, header['pincode'])))
            except Pincode.DoesNotExist:
                pincode = Pincode(
                    city=city,
                    pincode=int(worksheet.cell_value(row, header['pincode']))
                )
                pincode.save()

    upload_branch_pincode_file(file)


def upload_user_list_file(file):
    workbook = xlrd.open_workbook(file)
    worksheet = workbook.sheet_by_index(0)
    rows = worksheet.nrows
    cols = worksheet.ncols

    header = {}
    for row in range(0, rows):
        if row == 0:
            for col in range(0, cols):
                cell = str(worksheet.cell_value(0, col)).lower().strip()
                if cell == 'name':
                    header['name'] = col
                if cell == 'designation':
                    header['role'] = col
                if cell == 'phone':
                    header['phone'] = col
                if cell == 'branch':
                    header['branch'] = col
        else:
            username = re.sub('\s+', '.', str(worksheet.cell_value(row, header['name'])).lower().strip())
            password = username + str('@nuvoex')
            name = re.split('\s+', str(worksheet.cell_value(row, header['name'])).strip())
            first_name = name[0]
            last_name = ''
            for i in range(1, len(name)):
                last_name += name[i] + str(' ')
            branch = Branch.objects.get(branch_name=str(worksheet.cell_value(row, header['branch'])).strip())
            role = str(worksheet.cell_value(row, header['role'])).strip()
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = User(
                    username=username,
                    first_name=first_name,
                    last_name=last_name.strip(),
                    password=password
                )
                user.save()
                profile = Employee(
                    user=user,
                    branch=branch,
                    role=role,
                    phone=re.sub('\.[^.]*$', '', str(worksheet.cell_value(row, header['phone'])))
                )
                profile.save()


def upload_vehicle_list_file(file):
    workbook = xlrd.open_workbook(file)
    worksheet = workbook.sheet_by_index(0)
    rows = worksheet.nrows
    cols = worksheet.ncols

    header = {}
    for row in range(0, rows):
        if row == 0:
            for col in range(0, cols):
                cell = str(worksheet.cell_value(0, col)).lower().strip()
                if cell == 'vehicle':
                    header['vehicle'] = col
                if cell == 'branch':
                    header['branch'] = col
        else:
            vehicle_no = str(worksheet.cell_value(row, header['vehicle'])).strip()
            try:
                vehicle = Vehicle.objects.get(vehicle_no=vehicle_no)
            except Vehicle.DoesNotExist:
                vehicle = Vehicle(
                    vehicle_no=vehicle_no,
                    branch=Branch.objects.get(branch_name=str(worksheet.cell_value(row, header['branch'])).strip()),
                    vehicle_type='2W'
                )
                vehicle.save()


@receiver(models.signals.post_delete, sender=Manifest)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)


@receiver(models.signals.pre_save, sender=Manifest)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """Deletes file from filesystem
    when corresponding `MediaFile` object is changed.
    """
    if not instance.pk:
        return False

    try:
        old_file = Manifest.objects.get(pk=instance.pk).file
    except Manifest.DoesNotExist:
        return False

    new_file = instance.file
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


def generate_barcode(text):
    writer = ImageWriter()
    options = dict(module_height=9.0, text_distance=0.5, font_size=7, quiet_zone=2.0)
    ean = barcode.get('code39', text, writer=writer)
    dir = 'awb/barcode/'
    return ean.save(MEDIA_ROOT + dir + text, options)
    #return dir + text + '.png'

