from rest_framework import serializers
from reviews.models import Review, Comment


class ReviewSerializer(serializers.ModelSerializer):
    """
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )
    """

    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    """
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    """
    review = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'

class ApiSignupSerializer(serializers.Serializer):
    email=serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    

class ApiTokenSerializer(serializers.Serializer):
    confirmation_code=serializers.CharField(required=True)
    username = serializers.CharField(required=True)
