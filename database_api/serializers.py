from .models import Patient
from rest_framework import serializers

import datetime

class PatientSerializer(serializers.ModelSerializer):
    ID = serializers.ReadOnlyField(source='id')
    Name = serializers.CharField(max_length=100, source='name')
    Family = serializers.CharField(max_length=100, source='family', default='', allow_blank=True)
    Age = serializers.IntegerField(source='age', allow_null=True)
    PhoneNumber = serializers.CharField(max_length=100, source='phone_number', default='', allow_blank=True)
    NationalID = serializers.CharField(max_length=100, source='national_id', default='', allow_blank=True)
    Address = serializers.CharField(max_length=100, source='address', default='', allow_blank=True)
    Email = serializers.CharField(max_length=100, source='email', default='', allow_blank=True)
    PlaceOfBirth = serializers.CharField(max_length=100, source='place_of_birth', default='', allow_blank=True)
    SurgeryDate = serializers.DateField(source='surgery_date', allow_null=True)
    SurgeryDay = serializers.IntegerField(source='surgery_day', allow_null=True)
    SurgeryTime = serializers.IntegerField(source='surgery_time', allow_null=True)
    SurgeryType = serializers.CharField(max_length=100, source='surgery_type', default='', allow_blank=True)
    SurgeryArea = serializers.IntegerField(source='surgery_area', allow_null=True)
    SurgeryDescription = serializers.CharField(max_length=100, source='surgery_description', default='', allow_blank=True)
    SurgeryResult = serializers.IntegerField(source='surgery_result', allow_null=True)
    SurgeonFirst = serializers.CharField(max_length=100, source='surgeon_first', default='', allow_blank=True)
    SurgeonSecond = serializers.CharField(max_length=100, source='surgeon_second', default='', allow_blank=True)
    Resident = serializers.CharField(max_length=100, source='resident', default='', allow_blank=True)
    Hospital = serializers.CharField(max_length=100, source='hospital', default='', allow_blank=True)
    HospitalType = serializers.IntegerField(source='hospital_type', allow_null=True)
    HospitalAddress = serializers.CharField(max_length=100, source='hospital_address', default='', allow_blank=True)
    CT = serializers.IntegerField(source='ct', allow_null=True)
    MR = serializers.IntegerField(source='mr', allow_null=True)
    FMRI = serializers.IntegerField(source='fmri', allow_null=True)
    DTI = serializers.IntegerField(source='dti', allow_null=True)
    OperatorFirst = serializers.CharField(max_length=100, source='operator_first',  default='', allow_blank=True)
    OperatorSecond = serializers.CharField(max_length=100, source='operator_second', default='', allow_blank=True)
    StartTime = serializers.TimeField(source='start_time', allow_null=True)
    StopTime = serializers.TimeField(source='stop_time', allow_null=True)
    EnterTime = serializers.TimeField(source='enter_time', allow_null=True)
    ExitTime = serializers.TimeField(source='exit_time', allow_null=True)
    PatientEnterTime = serializers.TimeField(source='patient_enter_time', allow_null=True)
    HeadFixType = serializers.IntegerField(source='head_fix_type', allow_null=True)
    CancellationReason = serializers.CharField(max_length=100, source='cancellation_reason', default='', allow_blank=True)
    FileNumber = serializers.CharField(max_length=100, source='file_number', default='', allow_blank=True)
    DateOfHospitalAdmission = serializers.DateField(source='date_of_hospital_admission', allow_null=True)
    PaymentStatus = serializers.IntegerField(source='payment_status', allow_null=True)
    DateOfFirstContact = serializers.DateField(source='date_of_first_contact', allow_null=True)
    PaymentNote = serializers.CharField(max_length=100, source='payment_note', default='', allow_blank=True)
    FirstCaller = serializers.CharField(max_length=100, source='first_caller', default='', allow_blank=True)
    DateOfPayment = serializers.DateField(source='date_of_payment', allow_null=True)
    LastFourDigitsCard = serializers.CharField(max_length=100, source='last_four_digits_card', default='', allow_blank=True)
    CashAmount = serializers.CharField(max_length=100, source='cash_amount', default='', allow_blank=True)
    Bank = serializers.CharField(max_length=100, source='bank', default='', allow_blank=True)
    DiscountPercent = serializers.IntegerField(source='discount_percent', allow_null=True)
    ReasonForDiscount = serializers.CharField(max_length=100, source='reason_for_discount', default='', allow_blank=True)
    HealthPlanAmount = serializers.CharField(max_length=100, source='health_plan_amount', default='', allow_blank=True)
    TypeOfInsurance = serializers.CharField(max_length=100, source='type_of_insurance', default='', allow_blank=True)
    FinancialVerifier = serializers.CharField(max_length=100, source='financial_verifier', default='', allow_blank=True)
    ReceiptNumber = serializers.IntegerField(source='receipt_number', allow_null=True)
    FRE = serializers.IntegerField(source='fre', allow_null=True)


    date_fields = ['surgery_date', 'date_of_hospital_admission', 'date_of_first_contact', 'date_of_payment']
    def to_representation(self, instance):
        for field in self.date_fields:
            if getattr(instance, field) == datetime.date(1, 1, 1):
                setattr(instance, field, "2002-05-16") # Abolfazl's birthday (To congratulate him email: odaat.iaath@gmail.com)
        return super(PatientSerializer, self).to_representation(instance)

    def to_internal_value(self, data):
        for field in self.date_fields:
            rfield = self.fields[field].source
            if data.get(rfield) == '':
                data[rfield] = datetime.date(1, 1, 1)
        return super(PatientSerializer, self).to_internal_value(data)
            

    class Meta:
        model = Patient
        fields = (
            'ID', 'Name', 'Family', 'Age', 'PhoneNumber', 'NationalID', 'Address', 'Email', 'PlaceOfBirth', 'SurgeryDate',
            'SurgeryDay', 'SurgeryTime', 'SurgeryType', 'SurgeryArea', 'SurgeryDescription', 'SurgeryResult',
            'SurgeonFirst', 'SurgeonSecond', 'Resident', 'Hospital', 'HospitalType', 'HospitalAddress', 'CT', 'MR',
            'FMRI', 'DTI', 'OperatorFirst', 'OperatorSecond', 'StartTime', 'StopTime', 'EnterTime', 'ExitTime',
            'PatientEnterTime', 'HeadFixType', 'CancellationReason', 'FileNumber', 'DateOfHospitalAdmission',
            'PaymentStatus', 'DateOfFirstContact', 'PaymentNote', 'FirstCaller', 'DateOfPayment', 'LastFourDigitsCard',
            'CashAmount', 'Bank', 'DiscountPercent', 'ReasonForDiscount', 'HealthPlanAmount', 'TypeOfInsurance',
            'FinancialVerifier', 'ReceiptNumber', 'FRE'
        )

patient_variables_mapping = {key: value.source for key, value in PatientSerializer().fields.items()}
reversed_patient_variables_mapping = {value: key for key, value in patient_variables_mapping.items()}

