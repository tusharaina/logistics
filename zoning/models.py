from django.db import models
from common.models import Time_Model

# Create your models here.
class Zone(Time_Model):
    ZONE_CODE = (
        ('A', 'Zone A'),
        ('B', 'Zone B'),
        ('C', 'Zone C')
    )
    zone = models.CharField(choices=ZONE_CODE, max_length=1,unique=True)
    description = models.CharField(max_length=100)

    def __unicode__(self):
        return self.zone

class City(Time_Model):
    city = models.CharField(max_length=50,unique=True)
    state = models.CharField(max_length=50)

    def __unicode__(self):
        return self.city


class Pincode(Time_Model):
    pincode = models.IntegerField(max_length=6,unique=True)
    city = models.ForeignKey(City)

    def __unicode__(self):
        return unicode(self.pincode)

