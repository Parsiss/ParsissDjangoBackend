from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, Count, Case, When, F, OuterRef, Subquery

from django.db.models import TextField
from django.contrib.postgres.fields import ArrayField
import pytz

class Array(Subquery):
    template = 'ARRAY(%(subquery)s)'
    output_field = ArrayField(base_field=TextField())

from django.db.models.functions import Trim

from django.contrib.postgres.aggregates import ArrayAgg

from .serializers import EventSerialize, PatientSerializer, patient_variables_mapping, \
    reversed_patient_variables_mapping, CustomPatientSerializer
from .get_options import GetAllSelectOptions, GetAdaptiveFilterOptions
from .models import Patient

from CRMbackend import settings
# if settings.DEBUG is True:
#     from . import transfer

from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin, CreateModelMixin, DestroyModelMixin, ListModelMixin, RetrieveModelMixin

import json, sqlite3, datetime, xlwt



def CountSurgeries():
    return Patient.objects.values('national_id').annotate(
        surgery_count=Count('national_id'),
        success_count=Count(Case(When(surgery_result=1, then=1))),
        cancel_count=Count(Case(When(surgery_result=2, then=1))),
        failure_count=Count(Case(When(surgery_result=3, then=1)))
    ).annotate(
        cleaned_national_id=Trim('national_id')
    ).exclude(cleaned_national_id__in=['', '***', 'اتباع'])


def GetMoreThanOneSurgery():
    return CountSurgeries().filter(surgery_count__gt=1).values('national_id')
    # return Patient.objects.filter(national_id__in=national_ids).order_by('-surgery_date') 

def GetCanceledSurgeries():
    return CountSurgeries().filter(Q(cancel_count=F('surgery_count'))).values('national_id')

def GetDelayedSurgeries():
    return CountSurgeries().filter(Q(cancel_count__gt=0) & Q(success_count__gt=0)).values('national_id')

def GetOptions(request):
    basic_options = GetAllSelectOptions()
    return JsonResponse(basic_options, safe=False)


def GetFilters(request):
    basic_filters = GetAllSelectOptions()
    requested_fields = ['surgery_area', 'special_filters', 'surgery_result', 'hospital_type', 'payment_status']
    return JsonResponse({field: basic_filters[field] for field in requested_fields}, safe=False)


@csrf_exempt
def GetAdaptiveFilters(request):
    extra_fields = ['surgeon_first', 'hospital', 'operator_first']
    body = json.loads(request.body)
    for field in extra_fields:
        if field in body:
            del body[field]
    
    data = get_filtered_patients(body).order_by('-surgery_date')
    adaptive_options = GetAdaptiveFilterOptions(data, extra_fields)
    return JsonResponse(adaptive_options, safe=False)


class PatientListView(
    GenericAPIView,
    ListModelMixin,
    CreateModelMixin
):
    queryset = Patient.objects.all().order_by('-surgery_date')
    serializer_class = PatientSerializer
    lookup_field = 'id'

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


class PatientDetailView(
    GenericAPIView,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin
):
    queryset = Patient.objects.all().order_by('-surgery_date')
    serializer_class = PatientSerializer
    lookup_field = 'id'

    def get(self, request, id=None):
        return self.retrieve(request, id)

    def post(self, request, id=None):
        return self.update(request, id)

    def delete(self, request, id=None):
        return self.destroy(request, id)


def ready(request):
    rows = transfer.rows
    for row in rows:
        name, family, age = row[4], row[5], row[6]
        phone_number, national_id, address, email = row[7], row[8], row[9], row[10]
        place_of_birth, surgery_date, surgery_day = row[11], row[12], row[13]
        surgery_time, surgery_type, surgery_area = row[14], row[15], row[16]
        surgery_description, surgery_result, surgeon_first = row[17], row[18], row[19]
        surgeon_second, resident, hospital = row[20], row[21], row[22]
        hospital_type, hospital_address, ct = row[23], row[24], row[25]
        mr, fmri, dti, operator_first = row[26], row[27], row[28], row[29]
        operator_second, start_time, stop_time = row[30], row[31], row[32]
        enter_time, exit_time, patient_enter_time = row[33], row[34], row[35]
        head_fix_type, cancellation_reason, file_number = row[36], row[37], row[38]
        date_of_hospital_admission, payment_status, date_of_first_contact = row[39], row[40], row[41]
        payment_note, first_caller, date_of_payment = row[42], row[43], row[44]
        last_four_digits_card, cash_amount, bank = row[45], row[46], row[47]
        discount_percent, reason_for_discount, health_plan_amount = row[48], row[49], row[50]
        type_of_insurance, financial_verifier, _, _, _, fre = row[51], row[52], row[53], row[54], row[55], 0

        # set time to None if it is 0
        if surgery_time == 0:
            surgery_time = None

        if start_time == 0:
            start_time = None
        
        if stop_time == 0:
            stop_time = None
        
        if enter_time == 0:
            enter_time = None
        
        if exit_time == 0:
            exit_time = None
        
        if patient_enter_time == 0:
            patient_enter_time = None

        if surgery_date == 0:
            surgery_date = None
        
        if date_of_hospital_admission == 0:
            date_of_hospital_admission = None

        if date_of_first_contact == 0:
            date_of_first_contact = None
        
        if date_of_payment == 0:
            date_of_payment = None

        patient = Patient(
            name=name,
            family=family,
            age=age,
            phone_number=phone_number,
            national_id=national_id,
            address=address,
            email=email,
            place_of_birth=place_of_birth,
            surgery_date=surgery_date.date() if surgery_date else None,
            surgery_day=surgery_day,
            surgery_time=surgery_time,
            surgery_type=surgery_type,
            surgery_area=surgery_area,
            surgery_description=surgery_description,
            surgery_result=surgery_result,
            surgeon_first=surgeon_first,
            surgeon_second=surgeon_second,
            resident=resident,
            hospital=hospital,
            hospital_type=hospital_type,
            hospital_address=hospital_address,
            ct=ct,
            mr=mr,
            fmri=fmri,
            dti=dti,
            operator_first=operator_first,
            operator_second=operator_second,
            start_time=start_time,
            stop_time=stop_time,
            enter_time=enter_time,
            exit_time=exit_time,
            patient_enter_time=patient_enter_time,
            head_fix_type=head_fix_type,
            cancellation_reason=cancellation_reason,
            file_number=file_number,
            date_of_hospital_admission=date_of_hospital_admission.date() if date_of_hospital_admission else None,
            payment_status=payment_status,
            date_of_first_contact=date_of_first_contact.date() if date_of_first_contact else None,
            payment_note=payment_note,
            first_caller=first_caller,
            date_of_payment=date_of_payment.date() if date_of_payment else None,
            last_four_digits_card=last_four_digits_card,
            cash_amount=cash_amount,
            bank=bank,
            discount_percent=discount_percent,
            reason_for_discount=reason_for_discount,
            health_plan_amount=health_plan_amount,
            type_of_insurance=type_of_insurance,
            financial_verifier=financial_verifier,
            fre=fre
        )
        patient.save()
    return HttpResponse('ok')



def get_filtered_patients(filters):
    data = Patient.objects.all().annotate(
        cleaned_surgeon_first=Trim('surgeon_first'),
        cleaned_hospital=Trim('hospital'),
        cleaned_operator_first=Trim('operator_first'),
    )

    if filters == None:
        filters = {}
    
    for key, value in filters.items():
        if key == 'surgery_date':
            value = [datetime.datetime.fromtimestamp(item, tz=pytz.timezone('Asia/Tehran')) if item else None for item in value]
            value = [item.date() if item else None for item in value]
            if value[0] is not None and value[1] is not None:
                data = data.filter(surgery_date__range=(value[0], value[1]))
            elif value[0] is not None:
                data = data.filter(surgery_date__gte=value[0])
            elif value[1] is not None:
                data = data.filter(surgery_date__lte=value[1])
        else:
            if len(value) > 0:
                q = Q()
                for item in value:
                    if key in ['surgeon_first', 'hospital', 'operator_first']:
                        q |= Q(**{'cleaned_' + key: item})

                    elif key == 'special_filters':
                        if item == 1:
                            patients = GetDelayedSurgeries()
                            q |= Q(national_id__in=patients)
                        elif item == 2:
                            patients = GetCanceledSurgeries()
                            q |= Q(national_id__in=patients)
                    else:
                        q |= Q(**{key: item})
                data = data.filter(q)
    return data


@csrf_exempt
def GetFilteredReport(request):
    body = json.loads(request.body)
    filters = json.loads(body['filters'])
    print(filters)

    page_index = int(body['page_index'])
    page_size = int(body['page_size'])

    data = get_filtered_patients(filters).order_by('-surgery_date')
    serialize = PatientSerializer(data[page_index * page_size: (page_index + 1) * page_size], many=True)
    return JsonResponse({
        'data': serialize.data, 
        'total': data.count()
        }, 
        safe=False
    )

@csrf_exempt
def GetSearchReport(request):
    body = json.loads(request.body)
    filters = json.loads(body['filters'])

    data = get_filtered_patients(filters).order_by('-surgery_date')
    serialize = CustomPatientSerializer(data, many=True)
    return JsonResponse({
        'data': serialize.data,
        'total': data.count()
        },
        safe=False
    )

@csrf_exempt
def GetCalendarEvents(request):
    data = Patient.objects.order_by('-surgery_date')
    serialize = EventSerialize(data, many=True)
    return JsonResponse(serialize.data, safe=False)

@csrf_exempt
def GetFilteredReportExcel(request):
    body = json.loads(request.body)
    filters = json.loads(body['filters'])

    data = get_filtered_patients(filters).order_by('-surgery_date')
    serialize = PatientSerializer(data, many=True)
    return JsonResponse({
        'data': serialize.data,
        'total': data.count()
        },
        safe=False
    )


@csrf_exempt
def GetAutofillData(request):
    fields = [patient_variables_mapping[item] for item in json.loads(request.body)]
    data = Patient.objects.all()
    response = {
        reversed_patient_variables_mapping[field]: list(
            data.annotate(cleaned=Trim(field)).values('cleaned').annotate(count=Count('cleaned')).order_by('-count').values_list('cleaned', 'count')
        ) for field in fields
    }
    return JsonResponse(response, safe=False)
            
@csrf_exempt
def UploadDB(request):
    reqBody = request.body
    with open('temp.db', 'wb') as f:
        f.write(reqBody)
    db = sqlite3.connect('temp.db')
    cursor = db.cursor()
    cursor.execute('SELECT SurgeryForms.NationalCode, RegistrationData.Error FROM RegistrationData INNER JOIN SurgeryForms ON RegistrationData.PatientUid = SurgeryForms.PatientUid')
    joined_data = cursor.fetchall()
    for data in joined_data:
        national_id = data[0]
        fulldata = Patient.objects.filter(national_id=national_id).order_by('surgery_date')
        for patient in fulldata:
            if patient.fre == 0:
                patient.fre = round(data[1], 2)
                patient.save()
    cursor.execute('SELECT * FROM SurgeryForms')
    surgery_form_data = cursor.fetchall()
    for data in surgery_form_data:
        national_id = data[2]
        fulldata = Patient.objects.filter(national_id=national_id).order_by('surgery_date')
        for patient in fulldata:
            if patient.surgery_description == "":
                patient.surgery_description = data[9]
                patient.save()
    return HttpResponse(status=200)
