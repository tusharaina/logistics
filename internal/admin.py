from django.contrib import admin
from .models import *
# Register your models here.

class BranchAdmin(admin.ModelAdmin):
    list_display = ('branch_name', 'branch_manager', 'phone')
    search_fields = ['branch_name', 'branch_manager']


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'branch', 'phone')
    search_fields = ['user', 'role', 'branch', 'phone']
    list_filter = ['role', 'branch']


admin.site.register(Branch, BranchAdmin)
admin.site.register(Branch_Pincode)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Vehicle)