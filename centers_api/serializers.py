from rest_framework import serializers
from .models import Devices, Centers


class DeviceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    version = serializers.CharField()
    center = serializers.CharField(source='center.name', read_only=True)
    center_id = serializers.IntegerField(write_only=True)


    class Meta:
        model = Devices
        fields = ['id', 'version', 'center', 'center_id']


class CenterSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    devices = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='version'
    )


    class Meta:
        model = Centers
        fields = ['id', 'name', 'devices']
