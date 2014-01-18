#Manifest Sheet's random header dictionary
MANIFEST_HEADER_DICT = {
    'awb': ['awb number', 'request id', 'awb'],
    'order_id': ['order_number', 'order id', 'order no', 'order_number', 'client order no', 'client order id'],
    'customer_name': ['customer name', 'cnee name', 'consignor name', 'cust name'],
    'cnor_name': ['cnor_name', 'cnor name'],
    'invoice_no': ['invoice_no', 'invoice no', 'client invoice no'],
    'address_1': ['shipping_address1', 'consignor address 1', 'cust address line 1'],
    'address_2': ['shipping_address2', 'consignor address 2', 'cust address line 2'],
    'area': ['area', 'cust area'],
    'region': ['shipping_region'],
    'landmark': ['landmark'],
    'city': ['shipping_city', 'consignor city', 'shipping city', 'city', 'cust city'],
    'origin_pincode': ['origin pincode', 'origin_pincode', 'pincode'],
    'pincode': ['return location pin code', 'shipping_postcode', 'shipping postcode', 'cust pincode', 'pincode'],
    'phone_1': ['shipping_phone', 'mobile no.', 'phone 1', 'cust phone'],
    'phone_2': ['alternate contact no', 'alternate mobile number', 'phone 2', 'cust alt phone'],
    'package_value': ['grand_total', 'tot amt', 'package value'],
    'expected_amount': ['amount to be collected', 'cod amount', 'cash amount'],
    'weight': ['weight', 'wt'],
    'length': ['length'],
    'breadth': ['breadth'],
    'height': ['height'],
    'package_sku': ['item_sku', 'package sku'],
    'description': ['description', 'sku description', 'item_description', 'item description', 'package description'],
    'package_price': ['package price'],
    'preferred_pickup_date': ['preferred pickup date'],
    'preferred_pickup_time': ['preferred pickup time'],
    'category': ['category', 'coddod', 'payment mode']
}

MIS_HEADER = ['AWB', 'Client', 'Order ID', 'Consignee', 'Phone', 'Address', 'Category', 'Amount', 'COD Amount',
              'Weight', 'Delivery Branch', 'Pickup Branch', 'Dispatch Count', 'First Trial', 'First Pending',
              'First Dispatch', 'Last Dispatch', 'Current Status', 'First Scan Location', 'Date']

AWB_STATUS = (
    ('DR', 'Data Received'),
    ('ISC', 'In-Scanned'),
    ('PP', 'Pending for Pickup'),
    ('PC', 'Pick-up Complete'),
    ('INT', 'In-Transit'),
    ('ITR', 'In-Transit (Return)'),
    ('DCR', 'Pending for Delivery/DTO'),
    ('DRS', 'Dispatched'),
    ('DTO', 'Dispatched to Client'),
    ('DEL', 'Delivered/DTO\'d to Client'),
    ('CAN', 'Cancelled'),
    ('SCH', 'Scheduled'),
    ('RET', 'Returned'),
    ('RBC', 'Rejected by Client'),
    ('CB', 'Called Back'),
    ('DBC', 'Deferred by Customer'),
    ('CNA', 'Customer not Available')
)

AWB_RL_REMARKS = (
    ('Customer does not want to return', 'Customer does not want to return'),
    ('Client Process Delay', 'Client Process Delay'),
    ('Customer deferring more than 3 days', 'Customer deferring more than 3 days'),
    ('Customer wants replacement/refund first', 'Customer wants replacement/refund first'),
    ('Pickup already done by self/other courier', 'Pickup already done by self/other courier'),
    ('Couldn\'t speak to customer', 'Couldn\'t speak to customer'),
    ('Other', 'Other')
)

AWB_FL_REMARKS = (
    ('Customer doesn\'t want the product', 'Customer doesn\'t want the product'),
    ('Client Process Delay', 'Client Process Delay'),
    ('Customer away for a long time', 'Customer away for a long time'),
    ('Wants Open Delivery', 'Wants Open Delivery'),
    ('Payment related dispute', 'Payment related dispute'),
    ('Couldn\'t speak to customer', 'Couldn\'t speak to customer'),
    ('Other', 'Other')
)