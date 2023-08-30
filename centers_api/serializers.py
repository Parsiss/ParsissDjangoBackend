from rest_framework import serializers
from .models import Devices, Centers, Events, DeviceFiles


class DeviceFilesSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    filename = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    file = serializers.FileField()
    type = serializers.ChoiceField(choices=DeviceFiles.DeviceFileType)

    device_id = serializers.IntegerField(write_only=True)
    event_id = serializers.IntegerField(allow_null=True, write_only=True, required=False)


    class Meta:
        model = DeviceFiles
        fields = ['id', 'filename', 'file', 'device_id', 'event_id', 'created_at', 'type']



class DeviceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    version = serializers.CharField(required=False, allow_blank=True)
    bundle_version = serializers.CharField(required=False, allow_blank=True)
    windows_version = serializers.CharField(required=False, allow_blank=True)
    system_password = serializers.CharField(required=False, allow_blank=True)
    center = serializers.CharField(source='center.name', read_only=True)
    center_id = serializers.IntegerField()

    files = DeviceFilesSerializer(many=True, read_only=True)
    
    class Meta:
        model = Devices
        fields = ['id', 'name', 'files', 'version', 'windows_version', 'system_password', 'bundle_version', 'center', 'center_id']



class CenterSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    devices = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
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
    description = serializers.CharField(required=False, allow_blank=True)
    date = serializers.DateTimeField()
    type = serializers.ChoiceField(choices=Events.EventType)
    device_id = serializers.IntegerField()
    files = DeviceFilesSerializer(many=True, read_only=True)

    class Meta:
        model = Events
        fields = ['id', 'files', 'description', 'device_id', 'date', 'type']




