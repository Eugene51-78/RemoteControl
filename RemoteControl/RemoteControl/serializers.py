from rest_framework import serializers

class ModelSerializer(serializers.Serializer):
    model_text = serializers.CharField(max_length=200)
    pub_date = serializers.DateTimeField()