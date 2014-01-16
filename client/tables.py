import django_tables2 as tables
from client.models import Client, Client_Warehouse


class ClientTable(tables.Table):
    email = tables.Column(accessor='additional.email')
    client_code = tables.TemplateColumn(template_code='{{ record.client_code }}')
    pan_no = tables.Column(accessor='additional.pan_no')
    tan_no = tables.Column(accessor='additional.tan_no')
    scheduling_time = tables.Column(accessor='additional.scheduling_time')
    bank = tables.Column(accessor='additional.bank_name')
    account_no = tables.Column(accessor='additional.account_no')
    city = tables.Column(accessor='additional.city')
    address = tables.Column(accessor='additional.address')
    phone = tables.Column(accessor='additional.phone')

    class Meta:
        # add class="paleblue to <table> tag
        model = Client
        exclude = ['is_active', 'creation_date', 'on_update']
        attrs = {"class": "table table-striped table-bordered table-hover"}


class ClientWarehouseTable(tables.Table):
    class Meta:
        # add class="paleblue to <table> tag
        model = Client_Warehouse
        exclude = ['is_active', 'creation_date', 'on_update']
        attrs = {"class": "table table-striped table-bordered table-hover"}