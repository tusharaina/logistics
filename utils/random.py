def get_manifest_header_dict(val, header, col):
    dict = {}
    if val in header['awb']:
        dict['awb'] = col

    if val in header['order_id']:
        dict['order_id'] = col

    if val in header['customer_name']:
        dict['customer_name'] = col

    if val in header['invoice_no']:
        dict['invoice_no'] = col

    if val in header['address_1']:
        dict['address_1'] = col

    if val in header['address_2']:
        dict['address_2'] = col

    if val in header['area']:
        dict['area'] = col

    if val in header['city']:
        dict['city'] = col

    if val in header['pincode']:
        dict['pincode'] = col

    if val in header['phone_1']:
        dict['phone_1'] = col

    if val in header['phone_2']:
        dict['phone_2'] = col

    if val in header['package_value']:
        dict['package_value'] = col

    if val in header['package_price']:
        dict['package_price'] = col

    if val in header['expected_amount']:
        dict['expected_amount'] = col

    if val in header['weight']:
        dict['weight'] = col

    if val in header['length']:
        dict['length'] = col

    if val in header['breadth']:
        dict['breadth'] = col

    if val in header['height']:
        dict['height'] = col

    if val in header['description']:
        dict['description'] = col

    if val in header['package_sku']:
        dict['package_sku'] = col

    if val in header['category']:
        dict['category'] = col

    if val in header['priority']:
        dict['priority'] = col

    # if val in header['preferred_pickup_date']:
    #     dict['preferred_pickup_date'] = col
    #
    # if val in header['preferred_pickup_time']:
    #     dict['preferred_pickup_time'] = col

    return dict


def mis_header_into_field(header):
    fields = []

    for h in header:
        if h.lower() == 'awb':
            fields.append('awb')
        pass
