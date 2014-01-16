from django.contrib.auth.models import User
from django.forms import ModelForm, ModelChoiceField, forms, Select
from internal.models import Branch, Employee, Vehicle, Branch_Pincode
from zoning.models import City


class BranchForm(ModelForm):
    class Meta:
        model = Branch
        exclude = ['is_active']


class BranchPincodeForm(ModelForm):
    class Meta:
        model = Branch_Pincode
        exclude = ['is_active']


class EmployeeForm(ModelForm):
    supervisor = ModelChoiceField(queryset=Employee.objects.all(), required=False)
    branch = ModelChoiceField(queryset=Branch.objects.all(), required=False)
    city = ModelChoiceField(queryset=City.objects.all(), required=False)

    class Meta:
        model = Employee
        exclude = ['is_active']


class VehicleForm(ModelForm):
    driver_name = ModelChoiceField(queryset=User.objects.filter(profile__role='FE'), required=True)

    class Meta:
        model = Vehicle
        exclude = ['is_active']


class BranchDropDownForm(forms.Form):
    branch = ModelChoiceField(queryset=Branch.objects.all().order_by('id'),
                              widget=Select(
                                  attrs={'class': 'select2-choice', 'data-style': 'btn-inverse', 'data-width': '50px'}))
