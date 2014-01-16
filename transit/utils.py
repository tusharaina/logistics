from transit.models import TB, MTS
from internal.models import Branch, Branch_Pincode
from awb.models import AWB


def create_tb():
    pincode = AWB.objects.filter(status="SIS")
    print pincode


def generateId(self, *args):
    branch = ''
    for i in args:
        branch += ('0' * (2 - len(str(i))) + str(i))
    try:
        id = str(int(self.objects.latest('creation_date').pk) + 1)
    except self.DoesNotExist:
        id = '1'
    return self.__name__ + branch + ('0' * (5 - len(id))) + id