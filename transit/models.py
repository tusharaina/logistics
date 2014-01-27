from django.db import models
from django.contrib.auth.models import User
from common.models import Time_Model


class TB(Time_Model):
    TB_TYPE = (
        ('N', 'Normal'),
        ('M', 'Mixed')
    )
    tb_id = models.CharField(max_length=15, verbose_name='TB')
    origin_branch = models.ForeignKey('internal.Branch', related_name='origin')
    delivery_branch = models.ForeignKey('internal.Branch', related_name='delivery')
    type = models.CharField(choices=TB_TYPE, max_length=1, default='N')

    def __unicode__(self):
        return self.pk

    def get_current_mts(self):
        return self.tb_history.all().order_by('-creation_date').exclude(mts=None)[0].mts

    def get_current_branch(self):
        return self.tb_history.all().order_by('-creation_date').exclude(branch=None)[0].branch

    def get_current_status(self):
        if self.delivery_branch == self.get_current_branch():
            return 'Delivered'
        else:
            return 'Un-Delivered'

    def get_awb_count(self):
        return self.awb_status_set.all().count()


class TB_History(Time_Model):
    tb = models.ForeignKey('TB', related_name='tb_history')
    mts = models.ForeignKey('MTS', null=True, blank=True)
    branch = models.ForeignKey('internal.Branch', null=True, blank=True)


class MTS(Time_Model):
    MTS_STATUS = (
        ('D', 'Received'),
        ('U', 'Un-delivered'),
        ('R', 'Red Alert')
    )

    MTS_TYPE = (
        ('I', 'Internal'),
        ('E', 'External')
    )
    mts_id = models.CharField(max_length=15, verbose_name='MTS')
    from_branch = models.ForeignKey('internal.Branch', related_name='from')
    to_branch = models.ForeignKey('internal.Branch', related_name='to')
    status = models.CharField(choices=MTS_STATUS, max_length=1, default='U')
    type = models.CharField(choices=MTS_TYPE, max_length=1, default='I')

    def get_readable_choice(self):
        return dict(self.MTS_STATUS)[self.status]

    def __unicode__(self):
        return self.pk

    def get_tbs(self):
        return self.tb_history_set.all()

    def get_tbs_count(self):
        return self.tb_history_set.all().count()


class DRS(Time_Model):
    DRS_STATUS = (
        ('O', 'Open'),
        ('C', 'Closed'),
        ('R', 'Red Alert')
    )
    drs_id = models.CharField(max_length=15, verbose_name='DRS')
    fe = models.ForeignKey(User)
    vehicle = models.ForeignKey('internal.Vehicle')
    opening_km = models.CharField(max_length=20, null=True, blank=True)
    closing_km = models.CharField(max_length=20, null=True, blank=True)
    branch = models.ForeignKey('internal.Branch')
    status = models.CharField(choices=DRS_STATUS, default='O', max_length=1)

    def __unicode__(self):
        return self.drs_id

    def get_readable_choice(self):
        return dict(self.DRS_STATUS)[self.status]

    def get_awb_count(self):
        return self.awb_status_set.all().count()

    def get_all_awb_count(self):
        return self.awb_history_set.all().count()

    def get_awb_close_count(self):
        fl = self.awb_status_set.filter(
            status__in=['DEL', 'CAN', 'DCR', 'PC', 'CNA', 'DBC', 'RET', 'SCH', 'DTO']).exclude(
            awb__category='REV').count()
        rl = self.awb_status_set.filter(
            status__in=['DEL', 'CAN', 'DCR', 'PC', 'CNA', 'DBC', 'RET', 'SCH', 'DTO', 'TB', 'TBD', 'MTS', 'MTD'],
            awb__category='REV').count()
        return fl + rl

    def get_open_awb_count(self):
        return self.awb_status_set.filter(status__in=['DRS', 'PP']).count()

    def get_expected_amount(self):
        exp_amt = self.awb_status_set.filter(manifest__category='FL').exclude(status__in=['CAN', 'CNA', 'DBC', 'RET']) \
            .aggregate(expected_amount=models.Sum('awb__expected_amount'))['expected_amount']
        return exp_amt if exp_amt > 0 else '0.00'

    def get_collected_amount(self):
        coll_amt = self.awb_status_set.aggregate(collected_amt=models.Sum('collected_amt'))['collected_amt']
        return coll_amt if coll_amt is not None else 0


class DTO(Time_Model):
    DTO_STATUS = (
        ('O', 'Open'),
        ('C', 'Closed'),
        ('R', 'Red Alert')
    )
    dto_id = models.CharField(max_length=15)
    fe = models.ForeignKey(User)
    vehicle = models.ForeignKey('internal.Vehicle')
    branch = models.ForeignKey('internal.Branch')
    status = models.CharField(choices=DTO_STATUS, default='O', max_length=1)

    def get_awb_count(self):
        return self.awb_status_set.all().count()

    def get_awb_close_count(self):
        return self.awb_status_set.filter(status__in=['DEL', 'CAN', 'RBC', 'CB']).count()

    def get_readable_choice(self):
        return dict(self.DTO_STATUS)[self.status]

    def get_open_awb_count(self):
        return self.awb_status_set.filter(status='DTO').count()


class RTO(Time_Model):
    DTO_STATUS = (
        ('O', 'Open'),
        ('C', 'Closed'),
        ('R', 'Red Alert')
    )
    rto_id = models.CharField(max_length=15)
    fe = models.ForeignKey(User)
    vehicle = models.ForeignKey('internal.Vehicle')
    branch = models.ForeignKey('internal.Branch')
    status = models.CharField(choices=DTO_STATUS, default='O', max_length=1)

    def get_awb_count(self):
        return self.awb_status_set.all().count()

    def get_awb_close_count(self):
        return self.awb_status_set.filter(status__in=['RET', 'CAN']).count()

    def get_readable_choice(self):
        return dict(self.DTO_STATUS)[self.status]


def close_drs(id):
    drs = DRS.objects.get(pk=id)
    if drs.get_open_awb_count() == 0 and drs.closing_km != None:
        DRS.objects.filter(pk=id).update(status='C')
        return True
    else:
        return False


