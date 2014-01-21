from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.utils.formats import date_format
from common.models import Time_Model

# Create your models here.
class Manifest(Time_Model):
    STATUS = (
        ('O', 'Open'),
        ('I', 'In-Scanned'),
        ('C', 'Closed'),
        ('A', 'Alert')
    )
    CATEGORY = (
        ('FL', 'Forward Logistics'),
        ('RL', 'Reverse Logistics'),
        ('MP', 'Money Pickup')
    )
    client = models.ForeignKey('client.Client')
    uploaded_by = models.ForeignKey(User)
    warehouse = models.ForeignKey('client.Client_Warehouse')
    branch = models.ForeignKey('internal.Branch')
    status = models.CharField(choices=STATUS, default='O', max_length=1)
    category = models.CharField(choices=CATEGORY, max_length=2)
    file = models.FileField(upload_to='uploads/manifest/')

    def get_readable_choice(self):
        return dict(self.CATEGORY)[self.category]

    def get_expected_awb_count(self):
        return self.awb_status_set.count()

    def get_in_scanned_awb_count(self):
        return self.awb_status_set.exclude(status='DR').count()

    def get_dispatched_awb_count(self):
        return self.awb_status_set.exclude(status='DRS').count()

    def get_delivered_awb_count(self):
        return self.awb_status_set.filter(status='DEL').count()

    def __unicode__(self):
        return self.file


class AWB(Time_Model):
    AWB_TYPE = (('COD', 'COD'),
                ('REV', 'Reverse Pickup'),
                ('PRE', 'Prepaid'),
                ('MPU', 'Money Pickup'))
    AWB_PRIORITY = (('L', 'LOW'),
                    ('N', 'Normal'),
                    ('H', 'High'))
    awb = models.CharField(max_length=15, unique=True, verbose_name='AWB')
    order_id = models.CharField(max_length=20, null=True, blank=True)
    invoice_no = models.CharField(max_length=50, null=True, blank=True)
    customer_name = models.CharField(max_length=50, null=True, blank=True)
    address_1 = models.CharField(max_length=200, null=True, blank=True)
    address_2 = models.CharField(max_length=200, null=True, blank=True)
    area = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    pincode = models.ForeignKey('zoning.Pincode')
    phone_1 = models.CharField(max_length=15, null=True, blank=True)
    phone_2 = models.CharField(max_length=15, null=True, blank=True)
    package_value = models.CharField(max_length=10, null=True, blank=True)
    package_price = models.CharField(max_length=10, null=True, blank=True)
    expected_amount = models.FloatField(max_length=12, null=True, blank=True)
    weight = models.CharField(max_length=10, null=True, blank=True)
    length = models.CharField(max_length=10, null=True, blank=True)
    breadth = models.CharField(max_length=10, null=True, blank=True)
    height = models.CharField(max_length=10, null=True, blank=True)
    package_sku = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    category = models.CharField(choices=AWB_TYPE, max_length=3, null=True, blank=True)
    priority = models.CharField(choices=AWB_PRIORITY, max_length=1, default='N')
    barcode = models.ImageField(upload_to='awb/barcode/', null=True, blank=True)
    # preferred_pickup_date = models.CharField(max_length=20, null=True, blank=True)
    # preferred_pickup_time = models.CharField(max_length=20, null=True, blank=True)
    def get_priority(self):
        return dict(self.AWB_PRIORITY)[self.priority]

    def get_readable_choice(self):
        return dict(self.AWB_TYPE)[self.category]

    def get_delivery_branch(self):
        if self.category == 'REV':
            return self.awb_status.manifest.branch
        else:
            return self.pincode.branch_pincode.branch

    def get_pickup_branch(self):
        if self.category == 'REV':
            return self.pincode.branch_pincode.branch
        else:
            return ''

    def get_awb_history(self, internal=True):
        hist_dict = {}
        awb_hist = self.awb_history_set.order_by('-creation_date')
        i = 0
        for h in awb_hist:
            if h.status != None:
                hist_dict[i] = {}
                try:
                    hist_dict[i]['branch'] = h.branch.branch_name
                except AttributeError:
                    hist_dict[i]['branch'] = ''
                hist_dict[i]['status'] = get_awb_status('status', h.status, hist_dict[i]['branch'], self, internal)
                hist_dict[i]['time'] = date_format(h.creation_date, "SHORT_DATETIME_FORMAT")
                i = i + 1

            if h.tb != None:
                hist_dict[i] = {}
                hist_dict[i]['branch'] = h.tb.origin_branch.branch_name
                hist_dict[i]['status'] = get_awb_status('tb', h.tb.tb_id, hist_dict[i]['branch'], self, internal)
                hist_dict[i]['time'] = date_format(h.creation_date, "SHORT_DATETIME_FORMAT")
                i = i + 1

            if h.mts != None:
                hist_dict[i] = {}
                hist_dict[i]['branch'] = h.mts.from_branch.branch_name
                hist_dict[i]['status'] = get_awb_status('mts', h.mts.mts_id, hist_dict[i]['branch'], self, internal)
                hist_dict[i]['time'] = date_format(h.creation_date, "SHORT_DATETIME_FORMAT")
                i = i + 1

            if h.drs != None:
                hist_dict[i] = {}
                hist_dict[i]['branch'] = h.drs.branch.branch_name
                hist_dict[i]['status'] = get_awb_status('drs', h.drs.drs_id, hist_dict[i]['branch'], self, internal)
                hist_dict[i]['time'] = date_format(h.creation_date, "SHORT_DATETIME_FORMAT")
                i = i + 1

            if h.dto != None:
                hist_dict[i] = {}
                hist_dict[i]['branch'] = h.dto.branch.branch_name
                hist_dict[i]['status'] = get_awb_status('dto', h.dto.dto_id, hist_dict[i]['branch'], self, internal)
                hist_dict[i]['time'] = date_format(h.creation_date, "SHORT_DATETIME_FORMAT")
                i = i + 1

            if h.rto != None:
                hist_dict[i] = {}
                hist_dict[i]['branch'] = h.rto.branch.branch_name
                hist_dict[i]['status'] = get_awb_status('rto', h.rto.rto_id, hist_dict[i]['branch'], self, internal)
                hist_dict[i]['time'] = date_format(h.creation_date, "SHORT_DATETIME_FORMAT")
                i = i + 1

        return hist_dict


    def __unicode__(self):
        return self.awb

    def get_client(self):
        return self.awb_status.manifest.client.client_name


    def get_full_address(self):
        address = self.address_1
        if self.address_2 != '':
            address += ', ' + self.address_2
        address += ', ' + self.city
        return address.encode('utf-8')

    def get_drs_count(self):
        try:
            return self.awb_history_set.exclude(drs=None).count()
        except Exception:
            return ''

    def get_first_pending(self):
        try:
            return date_format(self.awb_history_set.filter(status='DCR').order_by('creation_date')[0].creation_date,
                               "SHORT_DATETIME_FORMAT")
        except Exception:
            return ''

    def get_first_dispatch(self):
        try:
            return date_format(self.awb_history_set.exclude(drs=None).order_by('creation_date')[0].creation_date,
                               "SHORT_DATETIME_FORMAT")
        except Exception:
            return ''

    def get_last_dispatch(self):
        try:
            return date_format(self.awb_history_set.exclude(drs=None).order_by('-creation_date')[0].creation_date,
                               "SHORT_DATETIME_FORMAT")
        except Exception:
            return ''

    def get_last_scan(self):
        if self.category == 'REV':
            try:
                return date_format(self.awb_history_set.exclude(dto=None).order_by('-creation_date')[0].creation_date,
                                   "SHORT_DATETIME_FORMAT")
            except Exception:
                return ''
        else:
            try:
                return date_format(self.awb_history_set.exclude(drs=None).order_by('-creation_date')[0].creation_date,
                                   "SHORT_DATETIME_FORMAT")
            except Exception:
                return ''

    def get_first_scan_branch(self):
        if self.category == 'REV':
            try:
                if self.get_pickup_branch() == self.get_delivery_branch():
                    return self.awb_history_set.filter(status='DCR').order_by('creation_date')[0].branch.branch_name
                else:
                    return self.awb_history_set.filter(status='PC').order_by('creation_date')[0].branch.branch_name
            except Exception:
                return ''
        else:
            try:
                return self.awb_history_set.filter(status='ISC').order_by('creation_date')[0].branch.branch_name
            except Exception:
                return ''

    def get_last_call_made_time(self):
        try:
            return date_format(
                self.awb_history_set.filter(status__in=['CAN', 'SCH', 'DBC', 'CB', 'RET'], branch=None).order_by(
                    '-creation_date')[0].creation_date, "SHORT_DATETIME_FORMAT")
        except Exception:
            return ''


    class Meta:
        verbose_name = 'AWB'


class AWB_Status(Time_Model):
    STATUS = (
        ('DR', 'Data Received'),
        ('PP', 'Pending for Pickup'),
        ('ISC', 'In-Scanned'),
        ('PS', 'Pick-up Scheduled'),
        ('PC', 'Pick-up Complete'),
        ('TB', 'TB Created'),
        ('TBD', 'TB Delivered'),
        ('MTS', 'MTS Created'),
        ('MTD', 'MTS Delivered'),
        ('DCR', 'Delivery Centre Reached'),
        ('DRS', 'DRS Created'),
        ('DTO', 'DTO Created'),
        ('DEL', 'Delivered'),
        ('CAN', 'Cancelled'),
        ('RET', 'Returned'),
        ('INT', 'In-Transit'),
        ('ITR', 'In-Transit (Return)'),
        ('DPR', 'Dispatched (Return)'),
        ('RET', 'Returned'),
        ('DBC', 'Deferred by Customer'),
        ('CNA', 'Customer not Available'),
        ('RBC', 'Rejected by Client'),
        ('CB', 'Called Back'),
        ('SCH', 'Scheduled')
    )
    awb = models.OneToOneField('AWB', related_name="awb_status")
    manifest = models.ForeignKey('Manifest', null=True, blank=True)
    current_branch = models.ForeignKey('internal.Branch', null=True, blank=True)
    current_tb = models.ForeignKey('transit.TB', null=True, blank=True)
    current_mts = models.ForeignKey('transit.MTS', null=True, blank=True)
    current_drs = models.ForeignKey('transit.DRS', null=True, blank=True)
    current_dto = models.ForeignKey('transit.DTO', null=True, blank=True)
    current_fe = models.ForeignKey('internal.Employee', null=True, blank=True)
    collected_amt = models.FloatField(max_length=12, null=True, blank=True)
    status = models.CharField(choices=STATUS, max_length=3, default='DR')
    zone = models.ForeignKey('zoning.Zone', null=True, blank=True)
    remark = models.CharField(max_length=200, blank=True, default='')
    reason = models.CharField(max_length=200, blank=True, default='')
    updated_by = models.ForeignKey(User, null=True, blank=True)

    def save(self, *args, **kwargs):
        AWB_History.objects.create(status=self.status, awb=self.awb)
        return super(AWB_Status, self).save(*args, **kwargs)

    def get_readable_choice(self):
        if self.status in ['TB', 'TBD', 'MTS', 'MTD']:
            return 'In-Transit'
        elif self.status == 'DCR':
            if self.manifest.category == 'FL':
                return 'Pending for Delivery'
            else:
                return 'Pending for DTO'
        elif self.status == 'DRS':
            return 'Dispatched'
        elif self.status == 'DTO':
            return 'Dispatched to Client'
        elif self.status == 'DEL' and self.manifest.category == 'RL':
            return "DTO'd to Client"
        else:
            return dict(self.STATUS)[self.status]

    def get_current_branch(self):
        return self.current_tb.get_current_branch

    def __unicode__(self):
        return self.awb.awb

    class Meta:
        verbose_name = 'AWB Status'


class AWB_History(Time_Model):
    awb = models.ForeignKey('AWB')
    tb = models.ForeignKey('transit.TB', null=True, blank=True)
    mts = models.ForeignKey('transit.MTS', null=True, blank=True)
    drs = models.ForeignKey('transit.DRS', null=True, blank=True)
    dto = models.ForeignKey('transit.DTO', null=True, blank=True)
    rto = models.ForeignKey('transit.RTO', null=True, blank=True)
    fe = models.ForeignKey('internal.Employee', null=True, blank=True)
    status = models.CharField(max_length=3, null=True, blank=True)
    branch = models.ForeignKey('internal.Branch', null=True, blank=True)


def get_awb_status(type, status, branch, awb, internal):
    if internal:
        branch_name = branch
    else:
        branch_name = get_branch_name(branch)
    if type == 'status':
        try:
            if awb.awb_status.updated_by.profile.role == 'CS':
                prefix = 'CS Call Made : '
            else:
                prefix = ''
        except Exception:
            prefix = ''
        if status == 'DR':
            return 'Data Received'
        elif status == 'ISC':
            if internal:
                return 'In-Scanned at ' + branch_name + ' branch'
            else:
                return 'Received at ' + branch_name + ' branch'
        elif status == 'DCR':
            if awb.category == 'REV':
                return 'Pending for DTO at ' + branch_name + ' branch'
            else:
                return 'Pending for Delivery at ' + branch_name + ' branch'
        elif status == 'RET':
            return prefix + 'Return'
        elif status == 'CAN':
            return prefix + 'Cancelled'
        elif status == 'DBC':
            return prefix + 'Deferred by Customer for Date : ' + awb.awb_status.reason
        elif status == 'CNA':
            return prefix + 'Customer not Available'
        elif status == 'CB':
            return prefix + 'Called Back at ' + branch_name + ' branch'
        elif status == 'RBC':
            return prefix + 'Rejected by Client'
        elif status == 'DEL':
            if awb.category == 'REV':
                if internal:
                    return "DTO'd to Client"
                else:
                    return 'Excepted by Client'
            else:
                return 'Delivered'
        elif status == 'PC':
            return 'Pickup Completed at ' + branch_name + ' branch'
        elif status == 'SCH':
            return prefix + 'Scheduled for Date : ' + awb.awb_status.reason
        else:
            return status
    else:
        if internal:
            return status + ' created at ' + branch_name + ' branch'
        else:
            if status[:2] == 'TB':
                return 'Transit Bag Created : In-Transit to ' + get_branch_name(
                    str(awb.get_delivery_branch().branch_name)) + ' branch'
            elif status[:2] == 'MT':
                return ''
            elif status[:2] == 'DR':
                if awb.category == 'REV':
                    return 'Pending for Pickup'
                else:
                    return 'Dispatched'
            elif status[:2] == 'DT':
                return 'Dispatched to client'
            elif status[:2] == 'RT':
                return 'Dispatched for RTO to client'


def get_rto_awbs(del_branch, curr_branch=None):
    if curr_branch is not None:
        return AWB.objects.filter(category__in=['COD', 'PRE'])


# def get_mis_fields(header):
#     from utils.random import mis_header_into_field
#
#     fields = mis_header_into_field(header)

def get_branch_name(branch):
    BRANCH_DICT = {'LXM': 'Laxminagar', 'SKT': 'Saket', 'GG1': 'Gurgaon', 'RAJ': 'Rajouri'}
    if branch in BRANCH_DICT:
        return BRANCH_DICT[branch]
    else:
        return branch