from django.contrib import admin
from awb.models import *
# Register your models here.

class AWBAdmin(admin.ModelAdmin):
    list_display = ('awb', 'customer_name', 'pincode')
    search_fields = ['awb', 'order_id']
    list_filter = ['pincode']


class AWB_StatusAdmin(admin.ModelAdmin):
    list_display = ('awb', 'status', 'current_branch')
    search_fields = ('awb', 'current_branch', 'current_tb')


admin.site.register(AWB, AWBAdmin)
admin.site.register(AWB_Status, AWB_StatusAdmin)
# admin.site.register(AWB_History)
admin.site.register(Manifest)

