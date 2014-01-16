from django.db import models
# Create your models here.

class Time_Model(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    on_update = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


#class Location(models.Model):
#    latitude = models.DecimalField(max_digits=3, decimal_places=6)
#    longitude = models.DecimalField(max_digits=3, decimal_places=6)
