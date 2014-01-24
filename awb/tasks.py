from time import gmtime, strftime
import csv

from celery.task import task
from django.http import HttpResponse
from django.utils.formats import date_format

from .models import AWB


@task
def generate_mis(mis, date):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="MIS_"' + str(strftime("%Y-%m-%d_%H-%M-%S",
                                                                                   gmtime())) + '".csv"'

    writer = csv.writer(response)
    header = ['AWB', 'Client', 'Order ID', 'Priority', 'Consignee', 'Address', 'Phone', 'Pincode', 'Category',
              'Amount', 'COD Amount', 'Weight', 'Delivery Branch', 'Pickup Branch', 'Dispatch Count',
              'First Pending', 'First Dispatch', 'Last Dispatch', 'Last Scan', 'Current Status',
              'Last Status on ' + date, 'First Scan Location', 'CS Call Made', 'Remark',
              'Reason',
              'Date']
    writer.writerow(header)
    for id in mis:
        awb = AWB.objects.get(pk=id)
        writer.writerow(
            [awb.awb, awb.get_client(), awb.order_id, awb.get_priority(), awb.customer_name,
             awb.get_full_address(),
             awb.phone_1, awb.pincode.pincode, awb.get_readable_choice(), awb.package_value,
             awb.expected_amount, awb.weight, awb.get_delivery_branch(), awb.get_pickup_branch(),
             awb.get_drs_count(), awb.get_first_pending(), awb.get_first_dispatch(), awb.get_last_dispatch(),
             awb.get_last_scan(), awb.awb_status.get_readable_choice(),
             awb.get_status_on_date(date),
             awb.get_first_scan_branch(), awb.get_last_call_made_time(), awb.awb_status.remark,
             awb.awb_status.reason, date_format(awb.creation_date, "SHORT_DATETIME_FORMAT")])
    return response
