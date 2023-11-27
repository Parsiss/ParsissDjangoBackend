from django.db import models
from django.db.models.functions import Trim
from django.db.models import Q
from simple_history.models import HistoricalRecords


class Patient(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default='')
    family = models.CharField(max_length=100, default='')
    age = models.IntegerField(null=True)
    phone_number = models.CharField(max_length=100, default='')
    national_id = models.CharField(max_length=100, default='')
    address = models.CharField(max_length=100, default='')
    email = models.CharField(max_length=100, default='')
    place_of_birth = models.CharField(max_length=100, default='')
    surgery_date = models.DateField(null=True)
    surgery_day = models.IntegerField(null=True)
    surgery_time = models.IntegerField(null=True)
    surgery_type = models.CharField(max_length=100, default='')
    surgery_area = models.IntegerField(null=True)
    surgery_description = models.TextField(default='')
    surgery_result = models.IntegerField(null=True)
    refund_status = models.CharField(max_length=100, default='')
    surgeon_first = models.CharField(max_length=100, default='')
    surgeon_second = models.CharField(max_length=100, default='')
    resident = models.CharField(max_length=100, default='')
    hospital = models.CharField(max_length=100, default='')
    hospital_type = models.IntegerField(null=True)
    hospital_address = models.CharField(max_length=100, default='')
    ct = models.IntegerField(null=True)
    mr = models.IntegerField(null=True)
    fmri = models.IntegerField(null=True)
    dti = models.IntegerField(null=True)
    operator_first = models.CharField(max_length=100, default='')
    operator_second = models.CharField(max_length=100, default='')
    start_time = models.TimeField(null=True)
    stop_time = models.TimeField(null=True)
    enter_time = models.TimeField(null=True)
    exit_time = models.TimeField(null=True)
    patient_enter_time = models.TimeField(null=True)
    head_fix_type = models.IntegerField(null=True)
    cancellation_reason = models.CharField(max_length=100, default='')
    file_number = models.CharField(max_length=100, default='')
    date_of_hospital_admission = models.DateField(null=True)
    payment_status = models.IntegerField(null=True)
    date_of_first_contact = models.DateField(null=True)
    payment_note = models.CharField(max_length=100, default='')
    first_caller = models.CharField(max_length=100, default='')
    date_of_payment = models.DateField(null=True)
    last_four_digits_card = models.CharField(max_length=100, default='')
    cash_amount = models.CharField(max_length=100, default='')
    bank = models.CharField(max_length=100, default='')
    discount_percent = models.FloatField(null=True)
    reason_for_discount = models.CharField(max_length=100, default='')
    health_plan_amount = models.CharField(max_length=100, default='')
    type_of_insurance = models.CharField(max_length=100, default='')
    financial_verifier = models.CharField(max_length=100, default='')
    receipt_number = models.IntegerField(null=True)
    fre = models.FloatField(null=True)
    history = HistoricalRecords()

    @property
    def previous_surgeries(self):
        # Calling this function is too expensive, use cautiously on large data
        return Patient.objects.annotate(
            cleaned_national_id=Trim('national_id')
        ).exclude(
            cleaned_national_id__in=['', '**', '***', 'اتباع']
        ).filter(~Q(surgery_date=self.surgery_date), cleaned_national_id=self.national_id,).values_list('surgery_date', 'surgery_result')

