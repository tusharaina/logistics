import xlrd
from zoning.models import City, Pincode

def upload_pincode_city_file(file):
    workbook = xlrd.open_workbook(file)
    worksheet = workbook.sheet_by_index(0)
    rows = worksheet.nrows
    cols = worksheet.ncols

    header = {}
    for row in range(0,rows):
        if row == 0:
            for col in range(0,cols):
                cell = str(worksheet.cell_value(0, col)).lower().strip()
                if cell == 'pincode':
                    header['pincode'] = col
                if cell == 'city':
                    header['city'] = col
                if cell == 'state':
                    header['state'] = col
        else:
            try:
                city = City.objects.get(city=str(worksheet.cell_value(row, header['city'])).strip())
            except City.DoesNotExist:
                city = City(
                    city = str(worksheet.cell_value(row, header['city'])).strip(),
                    state = str(worksheet.cell_value(row, header['state'])).strip()
                )
                city.save()
            try:
                pincode = Pincode.objects.get(pincode=int(worksheet.cell_value(row, header['pincode'])))
            except Pincode.DoesNotExist:
                pincode = Pincode(
                    city = city,
                    pincode = int(worksheet.cell_value(row, header['pincode']))
                )
                pincode.save()

