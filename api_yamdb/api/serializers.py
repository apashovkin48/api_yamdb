import re
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from reviews.models import Genre, Category, Title, Review, Comment

User = get_user_model()


def username_check(username):
    if username == 'me':
        raise serializers.ValidationError(
            {'username': 'Нельзя использовать me'})
    if not re.match(r'^[\w.@+-]+\Z', username):
        raise serializers.ValidationError(
            {'username': 'Required. 150 characters or fewer.'
                         'Letters, digits and @/./+/-/_ only.'}
        )


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        exclude = ('id',)
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        exclude = ('id',)
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class ReadOnlyTitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer для модели Review"""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = [
            'id',
            'text',
            'author',
            'score',
            'pub_date'
        ]

    def validate_score(self, value):
        if value < 1 or value > 10:
            raise serializers.ValidationError(
                'Недопустимое значение рейтинга!'
            )
        return value

    def validate(self, data):
        if self.context.get('request').method != 'PATCH':
            title = get_object_or_404(
                Title,
                id=self.context.get('view').kwargs.get('title_id')
            )
            author = self.context.get('request').user

            if title.reviews.filter(author=author).exists():
                raise serializers.ValidationError(
                    "Вы уже написали свой отзыв к данному произведению"
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Serializer для модели Comment"""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = [
            'id',
            'text',
            'author',
            'pub_date'
        ]


class ApiSignupSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        max_length=254
    )
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[username_check]
    )


class ApiTokenSerializer(serializers.Serializer):
    confirmation_code = serializers.CharField(required=True)
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[username_check]
    )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        ]


class MeSerilizer(UserSerializer):
    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)
