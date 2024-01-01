from requests import Response
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.mixins import UpdateModelMixin, CreateModelMixin, DestroyModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated

from .models import Devices, Centers, Events, DeviceFiles, DeviceHints
from .serializers import DeviceSerializer, CenterSerializer, EventsSerizlier, DeviceFilesSerializer, DeviceHintsSerializer

from rest_framework.decorators import permission_classes, api_view
from django.views.decorators.csrf import csrf_exempt

from django.db.models import Q, Count
from django.db.models.functions import Trim
from django.http import JsonResponse, HttpResponse


class CentersListView(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = Centers.objects.all()
    serializer_class = CenterSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class DeviceHintsDetailView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    queryset = DeviceHints.objects.all()
    serializer_class = DeviceHintsSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]


    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)



class DeviceHintsListView(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = DeviceHints.objects.all()
    serializer_class = DeviceHintsSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetAllHintsUniquely(request):
    hints = DeviceHints.objects.all().annotate(cleaned=Trim('description')).values('cleaned', 'is_essential').annotate(count=Count('description')).order_by('-count')
    hints = {('*' if hint['is_essential'] else '') + hint['cleaned']: hint['count']  for hint in hints}
    return JsonResponse(hints)


class CentersDetailView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    queryset = Centers.objects.all()
    serializer_class = CenterSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)



class DevicesListView(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = Devices.objects.all()
    serializer_class = DeviceSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)



class DevicesDetailView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    queryset = Devices.objects.all()
    serializer_class = DeviceSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)



class EventsListView(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = Events.objects.all()
    serializer_class = EventsSerizlier
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class EventsDetailView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    queryset = Events.objects.all()
    serializer_class = EventsSerizlier
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class EventsFilteredView(ListModelMixin, GenericAPIView):
    def get_queryset(self):
        return Events.objects.filter(device_id=self.kwargs['device_id'], parent__isnull=True)

    serializer_class = EventsSerizlier
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class DeviceFilesUploadView(CreateModelMixin, GenericAPIView):
    parser_classes = [MultiPartParser]
    queryset = DeviceFiles.objects.all()
    serializer_class = DeviceFilesSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)



class DeviceFilesDeleteView(DestroyModelMixin, GenericAPIView):
    queryset = DeviceFiles.objects.all()
    serializer_class = DeviceFilesSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)



class DeviceFilesView(ListModelMixin, GenericAPIView):
    serializer_class = DeviceFilesSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return DeviceFiles.objects.filter(device_id=self.kwargs['device_id'])

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
