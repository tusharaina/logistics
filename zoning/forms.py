from django.forms import ModelForm
from zoning.models import City, Pincode, Zone


class CityForm(ModelForm):
    class Meta:
        model = City
        fields = '__all__'


class PincodeForm(ModelForm):
    class Meta:
        model = Pincode
        fields = '__all__'


class ZoneForm(ModelForm):
    class Meta:
        model = Zone
        fields = '__all__'
