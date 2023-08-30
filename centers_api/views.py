from rest_framework.generics import GenericAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.mixins import UpdateModelMixin, CreateModelMixin, DestroyModelMixin, ListModelMixin, RetrieveModelMixin

from .models import Devices, Centers, Events, DeviceFiles
from .serializers import DeviceSerializer, CenterSerializer, EventsSerizlier, DeviceFilesSerializer

import json 




class CentersListView(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = Centers.objects.all()
    serializer_class = CenterSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)



class CentersDetailView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    queryset = Centers.objects.all()
    serializer_class = CenterSerializer
    lookup_field = 'id'

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

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)



class DevicesDetailView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    queryset = Devices.objects.all()
    serializer_class = DeviceSerializer
    lookup_field = 'id'

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

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class EventsDetailView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    queryset = Events.objects.all()
    serializer_class = EventsSerizlier
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class EventsFilteredView(ListModelMixin, GenericAPIView):
    def get_queryset(self):
        return Events.objects.filter(device_id=self.kwargs['device_id'])

    serializer_class = EventsSerizlier
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)



class DeviceFilesUploadView(CreateModelMixin, GenericAPIView):
    parser_classes = [MultiPartParser]
    queryset = DeviceFiles.objects.all()
    serializer_class = DeviceFilesSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)



class DeviceFilesDeleteView(DestroyModelMixin, GenericAPIView):
    queryset = DeviceFiles.objects.all()
    serializer_class = DeviceFilesSerializer
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)



class DeviceFilesView(ListModelMixin, GenericAPIView):
    serializer_class = DeviceFilesSerializer

    def get_queryset(self):
        return DeviceFiles.objects.filter(device_id=self.kwargs['device_id'])

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
