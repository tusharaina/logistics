import django_tables2 as tables
from transit.models import TB, MTS, DRS, DTO


class TBTable(tables.Table):
    current_mts = tables.Column(accessor='get_current_mts.mts_id', verbose_name='Current MTS')
    awb = tables.TemplateColumn(template_code='<a href="/transit/tb/{{ record.id }}">{{ record.get_awb_count }}</a>',
                                verbose_name='AWB')
    current_branch = tables.Column(accessor='get_current_branch.branch_name')
    status = tables.Column(accessor='get_current_status')
    #action = tables.TemplateColumn(
    #    template_code='<div class="hidden-phone visible-desktop btn-group"><button class="btn btn-mini btn-info" id="editTB"><i class="icon-edit bigger-120"></i></button></div>')

    class Meta:
        model = TB
        exclude = ['on_update', 'is_active', 'type', 'creation_date', 'id']
        attrs = {"class": "table table-striped table-bordered table-hover"}


class MTSTable(tables.Table):
    tb = tables.TemplateColumn(template_code='<a href="/transit/mts/{{ record.id }}">{{ record.get_tbs_count }}</a>')
    action = tables.TemplateColumn(
        template_code='<div class="hidden-phone visible-desktop btn-group"><button class="btn btn-mini btn-info" id="editMTS"><i class="icon-edit bigger-120"></i></button></div>')

    class Meta:
        model = MTS
        exclude = ['creation_date', 'on_update', 'is_active', 'id']
        attrs = {"class": "table table-striped table-bordered table-hover"}


class MTSOutgoingTable(tables.Table):
    tb = tables.TemplateColumn(template_code='<a href="/transit/mts/{{ record.id }}">{{ record.get_tbs_count }}</a>')

    class Meta:
        model = MTS
        exclude = ['creation_date', 'on_update', 'is_active', 'id']
        attrs = {"class": "table table-striped table-bordered table-hover"}


class DRSTable(tables.Table):
    drs_id = tables.TemplateColumn(
        template_code='<a href="/transit/drs/{{ record.id }}">{{ record.drs_id }}</a>', verbose_name='DRS')
    awb = tables.TemplateColumn(
        template_code='<a href="/transit/drs/{{ record.id }}">{{ record.get_awb_count }}</a>', verbose_name='AWB')
    #del_can = tables.Column(accessor='get_awb_delcan_count',verbose_name='Del/Can AWB')
    expected_amount = tables.Column(accessor='get_expected_amount')
    collected_amount = tables.Column(accessor='get_collected_amount')
    #action = tables.TemplateColumn(
    #    template_code='<div class="hidden-phone visible-desktop btn-group"><button class="btn btn-mini btn-info" id="editDRS"><i class="icon-edit bigger-120"></i></button></div>')

    class Meta:
        model = DRS
        exclude = ['creation_date', 'on_update', 'is_active']
        attrs = {"class": "table table-striped table-bordered table-hover"}


class DTOTable(tables.Table):
    dto_id = tables.TemplateColumn(
        template_code='<a href="/transit/dto/{{ record.id }}">{{ record.dto_id }}</a>', verbose_name='DTO')
    awb = tables.TemplateColumn(template_code='<a href="/transit/dto/{{ record.id }}">{{ record.get_awb_count }}</a>')
    #action = tables.TemplateColumn(
    #    template_code='<div class="hidden-phone visible-desktop btn-group"><button class="btn btn-mini btn-info" id="editDTO"><i class="icon-edit bigger-120"></i></button></div>')

    class Meta:
        model = DTO
        exclude = ['creation_date', 'on_update', 'is_active']
        attrs = {"class": "table table-striped table-bordered table-hover"}
