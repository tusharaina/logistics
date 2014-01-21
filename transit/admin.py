from django.contrib import admin
from transit.models import *
# Register your models here.

class DRSAdmin(admin.ModelAdmin):
    list_display = ('drs_id', 'branch', 'status', 'fe')
    search_fields = ['drs', 'branch', 'status', 'fe']
    list_filter = ['branch', 'status', 'fe']


admin.site.register(TB)
admin.site.register(MTS)
admin.site.register(DRS, DRSAdmin)
admin.site.register(DTO)

