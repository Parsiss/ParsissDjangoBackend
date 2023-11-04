from django.db.models import Count
from django.db.models.functions import Trim

from .models import Patient


def GetAllSelectOptions():
    surgeryDay = {
        'surgery_day': [
            {'Value': 1, 'Text': 'Saturday'},
            {'Value': 2, 'Text': 'Sunday'},
            {'Value': 3, 'Text': 'Monday'},
            {'Value': 4, 'Text': 'Tuesday'},
            {'Value': 5, 'Text': 'Wednesday'},
            {'Value': 6, 'Text': 'Thursday'},
            {'Value': 7, 'Text': 'Friday'},
        ]
    }

    surgerytime = {
        'surgery_time': [
            {'Value': 1, 'Text': 'Morning'},
            {'Value': 2, 'Text': 'Afternoon'},
            {'Value': 3, 'Text': 'Evening'},
            {'Value': 4, 'Text': 'Night'},
        ]
    }
    surgeryarea = {
        'surgery_area': [
            {'Value': 1, 'Text': 'Neurosurgery'},
            {'Value': 2, 'Text': 'ENT'},
            {'Value': 3, 'Text': 'ENT & Neurosurgery'},
            {'Value': 4, 'Text': 'CMF'},
            {'Value': 5, 'Text': 'Spine'},
            {'Value': 6, 'Text': 'Orthopedics'},
        ]
    }

    surgeryresult = {
        'surgery_result': [
            {'Value': 1, 'Text': 'Success'},
            {'Value': 2, 'Text': 'Canceled'},
            {'Value': 3, 'Text': 'Fail'},
        ]
    }

    specialfilters = {
        'special_filters': [
            {'Value': 1, 'Text': 'Delayed'},
            {'Value': 2, 'Text': 'Completely Cancelled'},
        ]
    }

    hospitaltype = {
        'hospital_type': [
            {'Value': 0, 'Text': 'Private'},
            {'Value': 1, 'Text': 'Governmental'},
            {'Value': 2, 'Text': 'Other'},
        ]
    }

    headfixtype = {
        'head_fix_type': [
            {'Value': 1, 'Text': 'Headband'},
            {'Value': 2, 'Text': 'Mayfield'},
            {'Value': 3, 'Text': 'Other'},
        ]
    }


    ImageStatus = [
        {'Value': 1, 'Text': 'Not Checked', 'Group': 'ct'},
        {'Value': 2, 'Text': 'Not Exist', 'Group': 'ct'},
        {'Value': 3, 'Text': 'Exist And Valid', 'Group': 'ct'},
        {'Value': 4, 'Text': 'Exist And Not Valid', 'Group': 'ct'},
    ]

    CT = { 'ct': ImageStatus }
    MR = { 'mr': ImageStatus }
    DTI = { 'dti': ImageStatus }
    FMRI = { 'fmri': ImageStatus }

    paymentstatus = {
        'payment_status': [
            {'Value': 1, 'Text': 'Paid'},
            {'Value': 2, 'Text': 'Not Paid'},
            {'Value': 3, 'Text': 'Free'},
            {'Value': 4, 'Text': 'Healthy Insurance'},
            {'Value': 5, 'Text': 'Paid By Hospital'},
        ]
    }



    return surgeryDay | surgerytime | surgeryarea | surgeryresult | hospitaltype | headfixtype | CT | MR | DTI | FMRI | paymentstatus | specialfilters


def GetAdaptiveFilterOptions(queryset, fields):
    extra_fields_values = {}

    for field in fields:
        data = queryset.annotate(cleaned=Trim(field)).values_list('cleaned').annotate(count=Count('cleaned')).order_by('-count')
        extra_fields_values[field] = [{
                'Value': txt,
                'Text': txt + ' (' + str(count) + ')',
            } for txt, count in data
        ]
    return extra_fields_values
