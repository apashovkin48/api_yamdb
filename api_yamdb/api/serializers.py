from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import *

class CategoryField(serializers.SlugRelatedField):
    pass


class CategorySerializer(serializers.ModelSerializer):
    pass


class GenreField(serializers.SlugRelatedField):
    pass


class GenreSerializer(serializers.ModelSerializer):
    pass


class TitleSerializer(serializers.ModelSerializer):
    pass


class ProfileSerializer(serializers.ModelSerializer):
    pass
