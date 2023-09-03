from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from django.db.models import Count, Case, When, Value, Q, Min, Sum
from django.db.models.functions import Trim

from database_api.models import Patient
from database_api.views import get_filtered_patients

from datetime import datetime
import json
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

@permission_classes([IsAuthenticated])
def FormatOperators(operators, types, surgeries):
    dict = { operator: {type: 0 for type in types } for operator in operators }
    for surgery in surgeries:
        dict[surgery[0]][surgery[1]] = surgery[2]
    
    for operator in operators:
        values = []
        for type in types:
            values.append(dict[operator][type])
        dict[operator] = values + [sum(values)]
    dict['مجموع'] = [sum([dict[operator][i] for operator in operators]) for i in range(len(types) + 1)]

    return dict


class OperatorsDatedReportView(View):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        start_date = datetime.fromtimestamp(int(request.GET['start_date']))
        end_date = datetime.fromtimestamp(int(request.GET['end_date']))

        patients = Patient.objects.filter(
            surgery_result=1,
            surgery_date__gte=start_date,
            surgery_date__lte=end_date
        ).annotate(
            operator_first_cleaned=Trim('operator_first'),
            hospital_cleaned=Trim('hospital')
        ).annotate(operator_first_cleaned=Case(
                When(operator_first_cleaned='', then=Value('بی نام')),
                default='operator_first_cleaned'
            )
        )

        operators = list(patients.values_list('operator_first_cleaned', flat=True).distinct().order_by('-operator_first_cleaned'))

        operators_surgeries = patients.annotate(result=Case(
            When(hospital_type=1, then=Value('دولتی')),
            When(Q(hospital_type=0) & ~Q(hospital_cleaned='تهران'), then=Value('خصوصی')),
            When(hospital_cleaned='تهران', then=Value('تهران')),
        )).values_list('operator_first_cleaned', 'result').annotate(count=Count(('result')))

        types = ['دولتی', 'خصوصی', 'تهران']

        result = FormatOperators(operators, types, list(operators_surgeries))
        return JsonResponse({
            'result': result,
            'types': types + ['مجموع']
        })



@csrf_exempt
@permission_classes([IsAuthenticated])
def GetHospitalsDatedReport(request, *args, **kwargs):
    body = json.loads(request.body)
    p1start_date = datetime.fromtimestamp(int(request.GET['p1start']))
    p1end_date = datetime.fromtimestamp(int(request.GET['p1end']))
    p2start_date = datetime.fromtimestamp(int(request.GET['p2start']))
    p2end_date = datetime.fromtimestamp(int(request.GET['p2end']))

    p1 = Q(surgery_date__gte=p1start_date, surgery_date__lte=p1end_date)
    p2 = Q(surgery_date__gte=p2start_date, surgery_date__lte=p2end_date)

    all_patients = get_filtered_patients(body)
    htypes = all_patients.filter(p1 | p2).annotate(
        htype=Case(
        When(hospital_type=1, then=Value('دولتی')),
        When(Q(hospital_type=0) & ~Q(cleaned_hospital='تهران'), then=Value('خصوصی')),
        When(cleaned_hospital='تهران', then=Value('تهران'))
    ))

    first_period = htypes.filter(p1).values_list('htype').annotate(period=Value('first_period'), count=Count('htype'))
    second_period = htypes.filter(p2).values_list('htype').annotate(period=Value('second_period'), count=Count('htype'))

    types = ['دولتی', 'خصوصی', 'تهران']
    periods = ['first_period', 'second_period']
    htypes = list(first_period) + list(second_period)

    hospitals = { period: {type: 0 for type in types } for period in periods }
    for hospital in htypes:
        hospitals[hospital[1]][hospital[0]] = hospital[2]
    
    for period in periods:
        values = []
        for type in types:
            values.append(hospitals[period][type])
        hospitals[period] = values

    for period in periods:
        hospitals[period] = hospitals[period] + [sum(hospitals[period])]
    
    return JsonResponse({
        **hospitals,
        'hospitals': types + ['مجموع']
    })


@csrf_exempt
@permission_classes([IsAuthenticated])
def GetPatientsDatedReport(request, *args, **kwargs):
    body = json.loads(request.body)
    p1start_date = datetime.fromtimestamp(int(request.GET['p1start']))
    p1end_date = datetime.fromtimestamp(int(request.GET['p1end']))
    p2start_date = datetime.fromtimestamp(int(request.GET['p2start']))
    p2end_date = datetime.fromtimestamp(int(request.GET['p2end']))

    p1 = Q(surgery_date__gte=p1start_date, surgery_date__lte=p1end_date)
    p2 = Q(surgery_date__gte=p2start_date, surgery_date__lte=p2end_date)

    all_patients = get_filtered_patients(body)
    htypes = all_patients.filter(p1 | p2).annotate(
        htype=Case(
        When(hospital_type=1, then=Value('دولتی')),
        When(Q(hospital_type=0) & ~Q(cleaned_hospital='تهران'), then=Value('خصوصی')),
        When(cleaned_hospital='تهران', then=Value('تهران'))
    ))

    first_period = htypes.filter(p1).values_list('htype').annotate(period=Value('first_period'), count=Count('national_id', distinct=True))
    second_period = htypes.filter(p2).values_list('htype').annotate(period=Value('second_period'), count=Count('national_id', distinct=True))

    types = ['دولتی', 'خصوصی', 'تهران']
    periods = ['first_period', 'second_period']
    htypes = list(first_period) + list(second_period)

    hospitals = { period: {type: 0 for type in types } for period in periods }
    for hospital in htypes:
        hospitals[hospital[1]][hospital[0]] = hospital[2]
    
    for period in periods:
        values = []
        for type in types:
            values.append(hospitals[period][type])
        hospitals[period] = values

    for period in periods:
        hospitals[period] = hospitals[period] + [sum(hospitals[period])]
    
    return JsonResponse({
        **hospitals,
        'hospitals': types + ['مجموع']
    })

@csrf_exempt
@permission_classes([IsAuthenticated])
def GetSuccessRateView(request):
    body = json.loads(request.body)
    patients = get_filtered_patients(body)
    success = patients.values('surgery_result').annotate(count=Count('surgery_result'))

    return JsonResponse({
        'count': list(success.values_list('count', flat=True)),
        'labels': list(success.values_list('surgery_result', flat=True))
    })
