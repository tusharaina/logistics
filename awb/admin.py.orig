from django.contrib import admin
from awb.models import *
# Register your models here.
<<<<<<< HEAD

class AWBAdmin(admin.ModelAdmin):
    list_display = ('awb', 'customer_name', 'pincode')
    search_fields = ['awb', 'order_id']
    list_filter = ['pincode']


class AWB_StatusAdmin(admin.ModelAdmin):
    list_display = (
        'awb', 'status', 'current_branch', 'current_drs')
    search_fields = ['awb__awb', 'current_branch__branch_name', 'current_tb__tb_id', 'current_drs__drs_id',
                     'current_mts__mts_id']
    list_filter = ['current_branch__branch_name', 'current_tb__tb_id', 'current_drs__drs_id',
                   'current_mts__mts_id']


class AWB_HistoryAdmin(admin.ModelAdmin):
    list_display = (
        'awb', 'status', 'branch', 'drs', 'tb', 'mts', 'dto')
    search_fields = ['awb__awb', 'branch__branch_name', 'tb__tb_id', 'drs__drs_id',
                     'mts__mts_id']
    list_filter = ['branch__branch_name', 'tb__tb_id', 'drs__drs_id',
                   'mts__mts_id']


admin.site.register(AWB, AWBAdmin)
admin.site.register(AWB_Status, AWB_StatusAdmin)
admin.site.register(AWB_History, AWB_HistoryAdmin)
admin.site.register(Manifest)

=======
#admin.site.register(AWB)
#admin.site.register(AWB_Status)
#admin.site.register(AWB_History)
#admin.site.register(Manifest)
>>>>>>> ed0e7ebb652bb805c35a217a89ce2e1e277fe64d
