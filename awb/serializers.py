from awb.models import AWB
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AWB
        fields = ('id', 'awb', 'order_id', 'invoice_no', 'customer_name')

