from rest_framework import serializers

class ApiSignupSerializer(serializers.Serializer):
    email=serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
class ApiTokenSerializer(serializers.Serializer):
    confirmation_code=serializers.CharField(required=True)
    username = serializers.CharField(required=True)
