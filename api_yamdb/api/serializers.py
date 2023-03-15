import re

from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

def username_check(username):
    if username=='me':
        raise serializers.ValidationError({'username':'Нельзя использовать '
                                                      'me'})
    if not re.match(r'^[\w.@+-]+\Z', username):
        raise serializers.ValidationError({'username': 'Required. 150 '
             'characters or fewer. Letters, digits and @/./+/-/_ only.'
            })
class ApiSignupSerializer(serializers.Serializer):
    email=serializers.EmailField(required=True, max_length=254)
    username = serializers.CharField(required=True, max_length=150,
                                     validators=[
        username_check])
class ApiTokenSerializer(serializers.Serializer):
    confirmation_code=serializers.CharField(required=True)
    username = serializers.CharField(required=True,max_length=150,  validators=[username_check])

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','email','first_name','last_name','bio','role']

class MeSerilizer(UserSerializer):
    class Meta(UserSerializer.Meta):
        read_only_fields=('role',)
