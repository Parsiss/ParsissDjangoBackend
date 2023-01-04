from django.http import JsonResponse, HttpResponse

from .serializers import PatientSerializer
from .get_options import GetAllSelectOptions
from .models import Patient
from . import transfer

from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin, CreateModelMixin, DestroyModelMixin, ListModelMixin, RetrieveModelMixin

import json, sqlite3


def GetOptions(request):
    data = GetAllSelectOptions()
    appended = []
    for data in data:
        appended.extend(data)
    return JsonResponse(appended, safe=False)


class PatientListView(
    GenericAPIView,
    ListModelMixin,
    CreateModelMixin
):
    queryset = Patient.objects.all()
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
    queryset = Patient.objects.all()
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
        id, name, family, age = row[0], row[4], row[5], row[6]
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
        type_of_insurance, financial_verifier, financial_verifier, fre = row[51], row[52], row[53], row[54]
        
        patient = Patient(
            id=id,
            name=name,
            family=family,
            age=age,
            phone_number=phone_number,
            national_id=national_id,
            address=address,
            email=email,
            place_of_birth=place_of_birth,
            surgery_date=surgery_date,
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
            date_of_hospital_admission=date_of_hospital_admission,
            payment_status=payment_status,
            date_of_first_contact=date_of_first_contact,
            payment_note=payment_note,
            first_caller=first_caller,
            date_of_payment=date_of_payment,
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


def GetFilteredReport(request):
    body = json.loads(request.body)
    data = Patient.objects.all().order_by('-surgery_date')
    for key, value in body.items():
        if key == 'surgery_date':
            if value[0] is not None and value[1] is not None:
                data = data.filter(surgery_date__range=(value[0], value[1]))
            elif value[0] is not None:
                data = data.filter(surgery_date__gte=value[0])
            elif value[1] is not None:
                data = data.filter(surgery_date__lte=value[1])
        else:
            if len(value) > 0:
                data = data.filter(**{key: value})
    data = PatientSerializer(data, many=True)
    return JsonResponse(data.data, safe=False)



def UploadDB(request):
    reqBody = request.body
    with open('temp.db', 'wb') as f:
        f.write(reqBody)
    db = sqlite3.connect('temp.db')
    cursor = db.cursor()
    cursor.execute('SELECT Table_PatientData.NationalCode, RegistrationData.Error FROM RegistrationData INNER JOIN Table_PatientData ON RegistrationData.PatientUid = Table_PatientData.PK_PatientUID')
    joined_data = cursor.fetchall()
    for data in joined_data:
        national_id = data[0]
        fulldata = Patient.objects.filter(national_id=national_id).order_by('surgery_date')
        for patient in fulldata:
            if patient.fre == 0:
                patient.fre = round(data[1], 2)
                patient.save()
    return HttpResponse(status=200)
