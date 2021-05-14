from rest_framework import serializers

class DeviceSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=20)
    quality = serializers.IntegerField()
    isReady = serializers.BooleanField()