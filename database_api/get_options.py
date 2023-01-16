from django.db.models import Count
from django.db.models.functions import Trim

from .models import Patient


def GetAllSelectOptions():
    surgeryDay = [
        {'Value': 1, 'Text': 'Saturday', 'Group': 'surgery_day'},
        {'Value': 2, 'Text': 'Sunday', 'Group': 'surgery_day'},
        {'Value': 3, 'Text': 'Monday', 'Group': 'surgery_day'},
        {'Value': 4, 'Text': 'Tuesday', 'Group': 'surgery_day'},
        {'Value': 5, 'Text': 'Wednesday', 'Group': 'surgery_day'},
        {'Value': 6, 'Text': 'Thursday', 'Group': 'surgery_day'},
        {'Value': 7, 'Text': 'Friday', 'Group': 'surgery_day'},
    ]

    surgerytime = [
        {'Value': 1, 'Text': 'Morning', 'Group': 'surgery_time'},
        {'Value': 2, 'Text': 'Afternoon', 'Group': 'surgery_time'},
        {'Value': 3, 'Text': 'Evening', 'Group': 'surgery_time'},
        {'Value': 4, 'Text': 'Night', 'Group': 'surgery_time'},
    ]

    surgeryarea = [
        {'Value': 1, 'Text': 'Neurosurgery', 'Group': 'surgery_area'},
        {'Value': 2, 'Text': 'ENT', 'Group': 'surgery_area'},
        {'Value': 3, 'Text': 'ENT & Neurosurgery', 'Group': 'surgery_area'},
        {'Value': 4, 'Text': 'CMF', 'Group': 'surgery_area'},
        {'Value': 5, 'Text': 'Spine', 'Group': 'surgery_area'},
        {'Value': 6, 'Text': 'Orthopedics', 'Group': 'surgery_area'},
    ]

    surgeryresult = [
        {'Value': 1, 'Text': 'Success', 'Group': 'surgery_result'},
        {'Value': 2, 'Text': 'Canceled', 'Group': 'surgery_result'},
        {'Value': 3, 'Text': 'Fail', 'Group': 'surgery_result'},
    ]

    hospitaltype = [
        {'Value': 0, 'Text': 'Private', 'Group': 'hospital_type'},
        {'Value': 1, 'Text': 'Governmental', 'Group': 'hospital_type'},
        {'Value': 2, 'Text': 'Other', 'Group': 'hospital_type'},
    ]

    headfixtype = [
        {'Value': 1, 'Text': 'Headband', 'Group': 'head_fix_type'},
        {'Value': 2, 'Text': 'Mayfield', 'Group': 'head_fix_type'},
        {'Value': 3, 'Text': 'Other', 'Group': 'head_fix_type'},
    ]

    CT = [
        {'Value': 1, 'Text': 'Not Checked', 'Group': 'ct'},
        {'Value': 2, 'Text': 'Not Exist', 'Group': 'ct'},
        {'Value': 3, 'Text': 'Exist And Valid', 'Group': 'ct'},
        {'Value': 4, 'Text': 'Exist And Not Valid', 'Group': 'ct'},
    ]

    MR = [
        {'Value': 1, 'Text': 'Not Checked', 'Group': 'mr'},
        {'Value': 2, 'Text': 'Not Exist', 'Group': 'mr'},
        {'Value': 3, 'Text': 'Exist And Valid', 'Group': 'mr'},
        {'Value': 4, 'Text': 'Exist And Not Valid', 'Group': 'mr'},
    ]

    DTI = [
        {'Value': 1, 'Text': 'Not Checked', 'Group': 'dti'},
        {'Value': 2, 'Text': 'Not Exist', 'Group': 'dti'},
        {'Value': 3, 'Text': 'Exist And Valid', 'Group': 'dti'},
        {'Value': 4, 'Text': 'Exist And Not Valid', 'Group': 'dti'},
    ]

    FMRI = [
        {'Value': 1, 'Text': 'Not Checked', 'Group': 'fmri'},
        {'Value': 2, 'Text': 'Not Exist', 'Group': 'fmri'},
        {'Value': 3, 'Text': 'Exist And Valid', 'Group': 'fmri'},
        {'Value': 4, 'Text': 'Exist And Not Valid', 'Group': 'fmri'},
    ]

    paymentstatus = [
        {'Value': 1, 'Text': 'Paid', 'Group': 'payment_status'},
        {'Value': 2, 'Text': 'Not Paid', 'Group': 'payment_status'},
        {'Value': 3, 'Text': 'Free', 'Group': 'payment_status'},
        {'Value': 4, 'Text': 'Healthy Insurance', 'Group': 'payment_status'},
        {'Value': 5, 'Text': 'Paid By Hospital', 'Group': 'payment_status'},
    ]



    return surgeryDay, surgerytime, surgeryarea, surgeryresult, hospitaltype, headfixtype, paymentstatus, CT, MR, DTI, FMRI


def GetAllCharOptions(queryset):
    extra_fields = ['surgeon_first', 'hospital', 'operator_first']
    extra_fields_values = []
    for field in extra_fields:
        field_valeus = []
        data = queryset.annotate(cleaned=Trim(field)).values_list('cleaned').annotate(count=Count('cleaned')).order_by('-count')
        
        for item in data:
            field_valeus.append({
                'Value': item[0],
                'Text': item[0] + ' (' + str(item[1]) + ')',
                'Group': field
            })
        extra_fields_values.append(field_valeus)
    return (*extra_fields_values, )
