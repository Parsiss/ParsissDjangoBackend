from rest_framework import serializers
from .models import Devices, Centers, Events


class DeviceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    version = serializers.CharField()
    center = serializers.CharField(source='center.name', read_only=True)
    center_id = serializers.IntegerField()

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
    devices_id = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='id',
        source='devices'
    )


    class Meta: 
        model = Centers
        fields = ['id', 'name', 'devices', 'devices_id']


class EventsSerizlier(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    description = serializers.CharField()
    date = serializers.DateTimeField()
    type = serializers.ChoiceField(choices=Events.EventType)
    device_id = serializers.IntegerField()

    class Meta:
        model = Events
        fields = ['id', 'description', 'device_id', 'date', 'type']
