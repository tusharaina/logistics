from django.contrib.auth.models import User
from django import forms
from transit.models import TB, MTS, DRS, DTO, RTO
from internal.models import Vehicle
#from awb.models import AWB

class CreateTBForm(forms.ModelForm):
    class Meta:
        model = TB
        exclude = ['is_active', 'type', 'tb_id', 'origin_branch']


class CreateMTSForm(forms.ModelForm):
    class Meta:
        model = MTS
        exclude = ['is_active', 'status', 'mts_id', 'from_branch']


class CreateDRSForm(forms.ModelForm):
    fe = forms.ModelChoiceField(queryset=User.objects.filter(profile__role='FE'), required=True)
    vehicle = forms.ModelChoiceField(queryset=Vehicle.objects.all())

    class Meta:
        model = DRS
        exclude = ['is_active', 'status', 'drs_id', 'branch', 'closing_km']


class CreateDTOForm(forms.ModelForm):
    fe = forms.ModelChoiceField(queryset=User.objects.filter(profile__role='FE'), required=True)
    vehicle = forms.ModelChoiceField(queryset=Vehicle.objects.all())

    class Meta:
        model = DTO
        exclude = ['is_active', 'status', 'dto_id', 'branch']

class CreateRTOForm(forms.ModelForm):
    fe = forms.ModelChoiceField(queryset=User.objects.filter(profile__role='FE'), required=True)
    vehicle = forms.ModelChoiceField(queryset=Vehicle.objects.all())

    class Meta:
        model=RTO
        exclude = ['is_active','status','rto_id','branch']