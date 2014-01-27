from django.db import models
# Create your models here.

class Time_Model(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    on_update = models.DateTimeField(auto_now=True, auto_now_add=True)
    is_active = models.BooleanField(default=True)


    class Meta:
        abstract = True
