from django.test import TestCase
def change_awb(i):
    k=10
    for j in i:
        if k==10:
            k=20
            j.type_of_awb='COD'
        elif k==20:
            j.type_of_awb='RL'
            k=30
        elif k==30:
            j.type_of_awb='PRE'
            k=10

    for j in i:
        j.save()

