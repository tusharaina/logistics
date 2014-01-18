import django_tables2 as tables
from django.contrib.auth.models import User


class UserTable(tables.Table):
    branch = tables.Column(accessor='profile.branch')
    role = tables.Column(accessor='profile.role')
    city = tables.Column(accessor='profile.city')
    address = tables.Column(accessor='profile.city')
    phone = tables.Column(accessor='profile.phone')

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')
        attrs = {"class": "table table-striped table-bordered table-hover"}

