from django.forms import ModelForm, TextInput, HiddenInput
from client.models import Client, Client_Additional, Client_Warehouse


class ClientForm(ModelForm):
    class Meta:
        model = Client
        exclude = ['is_active', 'awb_assigned_from', 'awb_assigned_to', 'awb_left']


class ClientAdditionalForm(ModelForm):
    class Meta:
        model = Client_Additional
        exclude = ['client', 'is_active']


class ClientWarehouseForm(ModelForm):
    class Meta:
        model = Client_Warehouse
        #widgets = {
        #    'pincode': TextInput(attrs={'id': 'warehouse_pincode'}),
        #}
        exclude = ['is_active']