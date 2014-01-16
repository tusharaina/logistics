import django_tables2 as tables
from internal.models import Branch, Vehicle, Employee, Branch_Pincode


class BranchTable(tables.Table):
    pincodes = tables.TemplateColumn(
        template_code='<a href="branch/{{ record.id }}/pincode">{{ record.get_pincode_count }}</a>')
    # action = tables.TemplateColumn(
    #     template_code='<div class="hidden-phone visible-desktop btn-group"><button class="btn btn-mini btn-info" id="editBranch"><i class="icon-edit bigger-120"></i></button></div>')

    class Meta:
        # add class="paleblue to <table> tag
        model = Branch
        exclude = ['creation_date', 'on_update', 'is_active']
        attrs = {"class": "table table-striped table-bordered table-hover"}


class BranchPincodeTable(tables.Table):
    class Meta:
        # add class="paleblue to <table> tag
        model = Branch_Pincode
        exclude = ['creation_date', 'on_update', 'is_active']
        attrs = {"class": "table table-striped table-bordered table-hover"}


class EmployeeTable(tables.Table):
    class Meta:
        # add class="paleblue to <table> tag
        model = Employee
        exclude = ['creation_date', 'on_update', 'is_active']
        attrs = {"class": "table table-striped table-bordered table-hover"}


class VehicleTable(tables.Table):
    class Meta:
        # add class="paleblue to <table> tag
        model = Vehicle
        exclude = ['creation_date', 'on_update', 'is_active']
        attrs = {"class": "table table-striped table-bordered table-hover"}