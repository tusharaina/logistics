from django.db import models
from common.models import Time_Model
# Create your models here.

class Client(Time_Model):
    CLIENT_TYPE = (
        ('C', 'Client'),
        ('S', 'SubClient')
    )
    client_code = models.CharField(max_length=3, unique=True)
    client_name = models.CharField(max_length=50, unique=True)
    client_type = models.CharField(choices=CLIENT_TYPE, max_length=1)
    awb_assigned_from = models.CharField(max_length=15)
    awb_assigned_to = models.CharField(max_length=15)
    awb_left = models.IntegerField(max_length=10)

    def __unicode__(self):
        return self.client_name


class Client_Additional(Time_Model):
    client = models.OneToOneField('client.Client', related_name='additional', unique=True)
    email = models.EmailField(max_length=50, blank=True, null=True)
    scheduling_time = models.CharField(null=True, blank=True, max_length=10)
    pan_no = models.CharField(max_length=50, blank=True, null=True)
    tan_no = models.CharField(max_length=50, blank=True, null=True)
    bank_name = models.CharField(max_length=50)
    account_no = models.CharField(max_length=50)
    city = models.ForeignKey('zoning.City', null=True, blank=True)
    address = models.CharField(max_length=50)
    phone = models.CharField(max_length=13)


class Client_Warehouse(Time_Model):
    warehouse_name = models.CharField(max_length=50, unique=True)
    client = models.ForeignKey('client.Client', related_name='warehouse')
    pincode = models.ForeignKey('zoning.Pincode')
    address = models.CharField(max_length=50)
    phone = models.CharField(max_length=13)

    def __unicode__(self):
        return self.warehouse_name


class Services(Time_Model):
    SERVICE_TYPES = (
        ('COD', 'COD'),
        ('PRE', 'Prepaid'),
        ('MPU', 'Money Pickup'),
        ('REV', 'Reverse Pickup')
    )
    service = models.CharField(choices=SERVICE_TYPES, max_length=3)
    description = models.CharField(max_length=50)


class Client_Services(Time_Model):
    client = models.ForeignKey('Client')
    service = models.ForeignKey('Services')




















    







