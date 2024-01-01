from rest_framework import serializers
from .models import DeviceHints, Devices, Centers, Events, DeviceFiles


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



class DeviceHintsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    description = serializers.CharField()
    device_id = serializers.IntegerField()
    is_essential = serializers.BooleanField()

    class Meta:
        model = DeviceHints 
        fields = ['id', 'description', 'device_id', 'is_essential']


class DeviceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    version = serializers.CharField(required=False, allow_blank=True)
    bundle_version = serializers.CharField(required=False, allow_blank=True)
    windows_version = serializers.CharField(required=False, allow_blank=True)
    system_password = serializers.CharField(required=False, allow_blank=True)
    center = serializers.CharField(source='center.name', read_only=True)
    center_id = serializers.IntegerField()

    model = serializers.CharField(required=False, allow_null=True)
    serial_number = serializers.CharField(required=False, allow_blank=True)
    installation_year = serializers.IntegerField(required=False, allow_null=True)

    hints = DeviceHintsSerializer(many=True, read_only=True)

    files = DeviceFilesSerializer(many=True, read_only=True)

    class Meta:
        model = Devices
        fields = '__all__'




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


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class EventsSerizlier(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    description = serializers.CharField(required=False, allow_blank=True)
    date = serializers.DateTimeField()
    type = serializers.ChoiceField(choices=Events.EventType)
    device_id = serializers.IntegerField()
    files = DeviceFilesSerializer(many=True, read_only=True)

    parent_id = serializers.IntegerField(allow_null=True, required=False)

    children = RecursiveField(many=True, read_only=True)
    can_have_children = serializers.BooleanField(read_only=True)

    class Meta:
        model = Events
        fields = ['id', 'files', 'description', 'device_id', 'date', 'type', 'parent_id', 'children', 'can_have_children']

