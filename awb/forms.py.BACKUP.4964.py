<<<<<<< HEAD
from django.forms import ModelForm, ModelChoiceField, Select
from .models import Manifest
from client.models import Client_Warehouse, Client


class UploadManifestForm(ModelForm):
    client = ModelChoiceField(queryset=Client.objects.all(),
                              widget=Select(attrs={'onchange': 'update_warehouse(this)'}))
    warehouse = ModelChoiceField(queryset=Client_Warehouse.objects.all())

=======
from django import forms
from .models import Manifest


class UploadManifestForm(forms.ModelForm):
>>>>>>> ed0e7ebb652bb805c35a217a89ce2e1e277fe64d
    class Meta:
        model = Manifest
        exclude = ['status', 'is_active', 'uploaded_by', 'branch']


