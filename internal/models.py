from django.db import models
from django.contrib.auth.models import User
from common.models import Time_Model
from awb.models import AWB

# Create your models here.
class Branch(Time_Model):
    branch_name = models.CharField(max_length=50, unique=True)
    branch_manager = models.OneToOneField(User, related_name='branch_employee', null=True, blank=True)
    city = models.ForeignKey('zoning.City', null=True, blank=True)
    address = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=13, null=True, blank=True)

    def __unicode__(self):
        return self.branch_name

    def get_awbs(self, status=[], type=''):
        branch_pincodes = self.branch_pincodes.all().select_related('pincode__awb')
        pincodes = []
        for branch_pincode in branch_pincodes:
            pincodes.append(branch_pincode.pincode)
        if status and type:
            awbs = AWB.objects.filter(category=type, awb_status__status__in=status, pincode__in=pincodes)
        else:
            awbs = AWB.objects.filter(pincode__in=pincodes)
        return awbs

    def get_pincode_count(self):
        return self.branch_pincodes.count()

    class Meta:
        verbose_name = 'Branch'


class Branch_Pincode(Time_Model):
    branch = models.ForeignKey('internal.Branch', related_name="branch_pincodes")
    pincode = models.OneToOneField('zoning.Pincode', related_name="branch_pincode")

    def __unicode__(self):
        return self.branch.branch_name


class Employee(Time_Model):
    USER_ROLE = (
        ('ADM', 'Admin'),
        ('OM', 'Operation Manager'),
        ('BM', 'Branch Manager'),
        ('FE', 'Field Executive'),
        ('FIN', 'Finance'),
        ('CS', 'Customer Service'),
        ('HR', 'HR'),
        ('CL', 'Client'),
        ('OT', 'Other'),
    )
    user = models.OneToOneField(User, related_name='profile')
    branch = models.ForeignKey('internal.Branch', null=True, blank=True)
    role = models.CharField(choices=USER_ROLE, max_length=3)
    city = models.ForeignKey('zoning.City', null=True, blank=True)
    address = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)

    def __unicode__(self):
        return self.user.first_name


class Vehicle(Time_Model):
    VEHICLE_TYPE = (
        ('2W', 'Two Wheeler'),
        ('3W', 'Three Wheeler'),
        ('4W', 'Four Wheeler'),
        ('HV', 'Heavy Vehicle')
    )
    vehicle_no = models.CharField(max_length=50, unique=True)
    vehicle_type = models.CharField(choices=VEHICLE_TYPE, max_length=2)
    driver_name = models.ForeignKey(User, blank=True, null=True)
    branch = models.ForeignKey(Branch, blank=True, null=True)

    def __unicode__(self):
        return self.vehicle_no


























