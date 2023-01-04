from django.http import JsonResponse
from django.views import View

from django.db.models import Count, Case, When, Value, Q
from django.db.models.functions import Trim

from database_api.models import Patient

from datetime import datetime


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


class MonthlyReportView(View):
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