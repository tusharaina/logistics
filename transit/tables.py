import itertools

import django_tables2 as tables

from transit.models import TB, MTS, DRS, DTO


class TBTable(tables.Table):
    def __init__(self, *args, **kwargs):
        super(TBTable, self).__init__(*args, **kwargs)
        self.counter = itertools.count()

    s_no = tables.Column(empty_values=(), verbose_name='S.No.', sortable=False, )
    current_mts = tables.Column(accessor='get_current_mts.mts_id', verbose_name='Current MTS', sortable=False, )
    awb = tables.TemplateColumn(template_code='<a href="/transit/tb/{{ record.id }}">{{ record.get_awb_count }}</a>',
                                verbose_name='AWB', sortable=False, )
    current_branch = tables.Column(accessor='get_current_branch.branch_name', sortable=False, )
    status = tables.Column(accessor='get_current_status', sortable=False, )
    date = tables.Column(accessor='creation_date', verbose_name='Date')
    #action = tables.TemplateColumn(
    #    template_code='<div class="hidden-phone visible-desktop btn-group"><button class="btn btn-mini btn-info" id="editTB"><i class="icon-edit bigger-120"></i></button></div>')

    class Meta:
        model = TB
        exclude = ['on_update', 'is_active', 'type', 'creation_date', 'id']
        attrs = {"class": "table table-striped table-bordered table-hover"}
        sequence = ('s_no',)

    def render_s_no(self):
        return next(self.counter) + 1


class MTSTable(tables.Table):
    def __init__(self, *args, **kwargs):
        super(MTSTable, self).__init__(*args, **kwargs)
        self.counter = itertools.count()

    s_no = tables.Column(empty_values=(), verbose_name='S.No.', sortable=False, )
    tb = tables.TemplateColumn(template_code='<a href="/transit/mts/{{ record.id }}">{{ record.get_tbs_count }}</a>',
                               verbose_name='TB', sortable=False, )
    action = tables.TemplateColumn(
        template_code='<div class="hidden-phone visible-desktop btn-group"><button class="btn btn-mini btn-info" id="editMTS"><i class="icon-edit bigger-120"></i></button></div>',
        sortable=False, )
    date = tables.Column(accessor='creation_date', verbose_name='Date')

    class Meta:
        model = MTS
        exclude = ['creation_date', 'on_update', 'is_active', 'id']
        attrs = {"class": "table table-striped table-bordered table-hover"}
        sequence = ('s_no',)

    def render_s_no(self):
        return next(self.counter) + 1


class MTSOutgoingTable(tables.Table):
    def __init__(self, *args, **kwargs):
        super(MTSOutgoingTable, self).__init__(*args, **kwargs)
        self.counter = itertools.count()

    s_no = tables.Column(empty_values=(), verbose_name='S.No.', sortable=False, )
    tb = tables.TemplateColumn(template_code='<a href="/transit/mts/{{ record.id }}">{{ record.get_tbs_count }}</a>',
                               verbose_name='TB', sortable=False, )
    date = tables.Column(accessor='creation_date', verbose_name='Date')

    class Meta:
        model = MTS
        exclude = ['creation_date', 'on_update', 'is_active', 'id']
        attrs = {"class": "table table-striped table-bordered table-hover"}
        sequence = ('s_no',)

    def render_s_no(self):
        return next(self.counter) + 1


class DRSTable(tables.Table):
    def __init__(self, *args, **kwargs):
        super(DRSTable, self).__init__(*args, **kwargs)
        self.counter = itertools.count()

    s_no = tables.Column(empty_values=(), verbose_name='S.No.', sortable=False, )
    drs_id = tables.TemplateColumn(
        template_code='<a href="/transit/drs/{{ record.id }}" target="_blank">{{ record.drs_id }}</a>',
        verbose_name='DRS')
    awb = tables.TemplateColumn(
        template_code='<a href="/transit/drs/{{ record.id }}">{{ record.get_awb_count }}</a>', verbose_name='AWB',
        sortable=False)
    open_awb = tables.TemplateColumn(
        template_code='<a href="/transit/drs/{{ record.id }}">{{ record.get_open_awb_count }}</a>', verbose_name='Open',
        sortable=False)
    expected_amount = tables.Column(accessor='get_expected_amount', sortable=False)
    collected_amount = tables.Column(accessor='get_collected_amount', sortable=False)
    date = tables.Column(accessor='creation_date', verbose_name='Date')
    #action = tables.TemplateColumn(
    #    template_code='<div class="hidden-phone visible-desktop btn-group"><button class="btn btn-mini btn-info" id="editDRS"><i class="icon-edit bigger-120"></i></button></div>')

    class Meta:
        model = DRS
        exclude = ['id', 'creation_date', 'on_update', 'is_active']
        sequence = ('s_no',)
        attrs = {"class": "table table-striped table-bordered table-hover"}

    def render_s_no(self):
        return next(self.counter) + 1


class DTOTable(tables.Table):
    def __init__(self, *args, **kwargs):
        super(DTOTable, self).__init__(*args, **kwargs)
        self.counter = itertools.count()

    s_no = tables.Column(empty_values=(), verbose_name='S.No.', sortable=False, )
    dto_id = tables.TemplateColumn(
        template_code='<a href="/transit/dto/{{ record.id }}">{{ record.dto_id }}</a>', verbose_name='DTO')
    awb = tables.TemplateColumn(template_code='<a href="/transit/dto/{{ record.id }}">{{ record.get_awb_count }}</a>',
                                verbose_name='AWB', sortable=False)
    open_awb = tables.TemplateColumn(
        template_code='<a href="/transit/drs/{{ record.id }}">{{ record.get_open_awb_count }}</a>',
        verbose_name='Open', order_by='dto_id', sortable=False)
    date = tables.Column(accessor='creation_date', verbose_name='Date')
    #action = tables.TemplateColumn(
    #    template_code='<div class="hidden-phone visible-desktop btn-group"><button class="btn btn-mini btn-info" id="editDTO"><i class="icon-edit bigger-120"></i></button></div>')

    class Meta:
        model = DTO
        exclude = ['creation_date', 'on_update', 'is_active', 'id']
        attrs = {"class": "table table-striped table-bordered table-hover"}
        sequence = ('s_no',)

    def render_s_no(self):
        return next(self.counter) + 1
