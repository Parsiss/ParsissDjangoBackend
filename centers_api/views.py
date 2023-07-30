from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin, CreateModelMixin, DestroyModelMixin, ListModelMixin, RetrieveModelMixin

from .models import Devices, Centers
from .serializers import DeviceSerializer, CenterSerializer

class CentersDetailView(ListModelMixin, CreateModelMixin, DestroyModelMixin, GenericAPIView):
    queryset = Centers.objects.all()
    serializer_class = CenterSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)



class DevicesView(ListModelMixin, CreateModelMixin, DestroyModelMixin, GenericAPIView):
    queryset = Devices.objects.all()
    serializer_class = DeviceSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

