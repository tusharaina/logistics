import django_tables2 as tables
from zoning.models import City, Pincode, Zone

class CityTable(tables.Table):

    class Meta:
        # add class="paleblue to <table> tag
        model = City
        exclude = ['creation_date','on_update','is_active']
        attrs = {"class": "table table-bordered table-condensed table-responsive table-stripped" }


class PincodeTable(tables.Table):

    class Meta:
        # add class="paleblue to <table> tag
        model = Pincode
        exclude = ['creation_date','on_update','is_active']
        attrs = {"class": "table table-bordered table-condensed table-responsive table-stripped" }


class ZoneTable(tables.Table):

    class Meta:
        # add class="paleblue to <table> tag
        model = Zone
        exclude = ['creation_date','on_update','is_active']
        attrs = {"class": "table table-bordered table-condensed table-responsive table-stripped" }