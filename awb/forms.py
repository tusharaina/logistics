from django.forms import ModelForm, ModelChoiceField, Select
from .models import Manifest
from client.models import Client_Warehouse, Client


class UploadManifestForm(ModelForm):
    client = ModelChoiceField(queryset=Client.objects.all(),
                              widget=Select(attrs={'onchange': 'update_warehouse(this)'}))
    warehouse = ModelChoiceField(queryset=Client_Warehouse.objects.all())

    class Meta:
        model = Manifest
        exclude = ['status', 'is_active', 'uploaded_by', 'branch']


