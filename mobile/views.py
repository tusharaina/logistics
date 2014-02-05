#from django.shortcuts import render
# Create your views here.
from django.core import serializers
from django.http import HttpResponse
from awb.models import AWB
# Create your views here.
def aw(request):
    data = serializers.serialize("json", AWB.objects.filter(awb_status__current_drs__fe=request.user))
    return HttpResponse(data, content_type="application/json")

def awb_history_mobile(request, awb_id):
        data = serializers.serialize('json', AWB.objects.filter(id=int(awb_id)))
        return HttpResponse(data, mimetype='application/json')
