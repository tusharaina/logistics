import django_tables2 as tables
from awb.models import AWB, Manifest


class AWBTable(tables.Table):
    awb = tables.TemplateColumn(
        template_code='<a href="/transit/awb/{{ record.id }}" >{{ record.awb }}</a>')
    client = tables.Column(accessor='awb_status.manifest.client')
    category = tables.Column(accessor='category')
    address = tables.TemplateColumn(template_code='{{ record.address_1 }}, {{ record.address_2 }}, {{ record.city }}')
    status = tables.Column(accessor='awb_status.get_readable_choice', order_by='awb_status__status')
    drs = tables.Column(accessor='awb_status.current_drs', verbose_name='DRS',
                        order_by='awb_status__current_drs__drs_id')
    current_branch = tables.Column(accessor='awb_status.current_branch.branch_name')
    delivery_branch = tables.Column(accessor='get_delivery_branch.branch_name',
                                    verbose_name='Delivery Branch',
                                    order_by='pincode__branch_pincode__branch__branch_name')

    class Meta:
        model = AWB
        fields = ('awb', 'order_id')
        attrs = {"class": "table table-striped table-bordered table-hover table-condensed"}


class AWBFLTable(tables.Table):
    awb = tables.TemplateColumn(
        template_code='<a href="/transit/awb/{{ record.id }}" >{{ record.awb }}</a>')
    client = tables.Column(accessor='awb_status.manifest.client.client_name')
    category = tables.Column(accessor='category')
    address = tables.TemplateColumn(template_code='{{ record.address_1 }}, {{ record.address_2 }}, {{ record.city }}')
    status = tables.Column(accessor='awb_status.get_readable_choice', order_by='awb_status__status')
    current_branch = tables.Column(accessor='awb_status.current_branch.branch_name')
    delivery_branch = tables.Column(accessor='get_delivery_branch.branch_name', verbose_name='Delivery Branch',
                                    order_by='pincode__branch_pincode__branch__branch_name')

    class Meta:
        model = AWB
        fields = ('awb', 'order_id', 'customer_name', 'address', 'pincode')
        attrs = {"class": "table table-striped table-bordered table-hover table-condensed"}

class AWBCODTable(tables.Table):
    awb = tables.TemplateColumn(
        template_code='<a href="/transit/awb/{{ record.id }}" >{{ record.awb }}</a>')
    expected_amt = tables.Column(accessor='expected_amount')

    class Meta:
        model = AWB
        fields = ('awb', 'order_id', 'customer_name', 'pincode')
        attrs = {"class": "table table-striped table-bordered table-hover table-condensed"}


class AWBRLTable(tables.Table):
    awb = tables.TemplateColumn(
        template_code='<a href="/transit/awb/{{ record.id }}" >{{ record.awb }}</a>')
    client = tables.Column(accessor='awb_status.manifest.client.client_name')
    category = tables.Column(accessor='category')
    address = tables.TemplateColumn(template_code='{{ record.address_1 }}, {{ record.address_2 }}, {{ record.city }}')
    status = tables.Column(accessor='awb_status.get_readable_choice', order_by='awb_status__status')
    pickup_branch = tables.Column(accessor='get_pickup_branch.branch_name', verbose_name='Pick-up Branch',
                                  order_by='pincode__branch_pincode__branch__branch_name')
    current_branch = tables.Column(accessor='awb_status.current_branch.branch_name')
    dto_branch = tables.Column(accessor='get_delivery_branch.branch_name', verbose_name='DTO Branch',
                               order_by='awb_status__manifest__branch__branch_name')

    class Meta:
        model = AWB
        fields = ('awb', 'order_id', 'customer_name', 'address', 'pincode',)
        attrs = {"class": "table table-striped table-bordered table-hover table-condensed"}


class ManifestTable(tables.Table):
    id = tables.TemplateColumn(
        template_code='<a href="/transit/manifest/{{ record.id }}" >{{ record.id }}</a>')
    awb_expected = tables.Column(accessor='get_expected_awb_count')
    awb_arrived = tables.Column(accessor='get_in_scanned_awb_count')
    awb_delivered = tables.Column(accessor='get_delivered_awb_count')

    class Meta:
        model = Manifest
        fields = ('id', 'client', 'status', 'category', 'uploaded_by', 'branch')
        attrs = {"class": "table table-striped table-bordered table-hover table-condensed"}

