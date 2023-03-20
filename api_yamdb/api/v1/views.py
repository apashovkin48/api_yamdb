from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (
    filters,
    mixins,
    permissions,
    status,
    viewsets,
)
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import (
    Category,
    Genre,
    Review,
    Title,
)
from .filters import TitlesFilter
from .permissions import (
    IsOnlyAdmin,
    IsAdminOrReadOnly,
    IsAuthorOrAdminOrModeratorReadOnly,
)
from .serializers import (
    ApiSignupSerializer,
    ApiTokenSerializer,
    CommentSerializer,
    CategorySerializer,
    GenreSerializer,
    MeSerilizer,
    ReadOnlyTitleSerializer,
    ReviewSerializer,
    TitleSerializer,
    UserSerializer,
)

User = get_user_model()


class TitleViewSet(viewsets.ModelViewSet):
    """ViewSet для title"""
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    serializer_class = TitleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitlesFilter
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return ReadOnlyTitleSerializer
        return TitleSerializer


class GenreViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    """ViewSet для Genre"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)


class CategoryViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    """ViewSet для Category"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Review"""
    serializer_class = ReviewSerializer
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = (IsAuthorOrAdminOrModeratorReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Comment"""
    serializer_class = CommentSerializer
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = (IsAuthorOrAdminOrModeratorReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


@api_view(['POST'])
def api_signup(request):
    serializer = ApiSignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data.get('email')
    username = serializer.validated_data.get('username')

    user, created = User.objects.get_or_create(email=email, username=username)

    send_mail(
        subject='Код подтверждения',
        message=f'Код подтверждения: {user.confirmation_code}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email]
    )
    return Response(serializer.validated_data, status=status.HTTP_200_OK)


@api_view(['POST'])
def api_token(request):
    serializer = ApiTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    confirmation_code = serializer.validated_data.get('confirmation_code')
    username = serializer.validated_data.get('username')

    user = get_object_or_404(User, username=username)
    if confirmation_code != user.confirmation_code:
        return Response({'confirmation_code': "Отсутствует обязательное поле "
                                              "или оно некорректно"},
                        status=status.HTTP_400_BAD_REQUEST)
    return Response({
        'Token': f'Bearer {str(AccessToken.for_user(user))}'
    })


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ('get', 'post', 'patch', 'delete')
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    permission_classes = (IsOnlyAdmin,)

    @action(methods=('get', 'patch'),
            detail=False, permission_classes=(permissions.IsAuthenticated,))
    def me(self, request):
        serilizer = MeSerilizer(
            self.request.user,
            request.data,
            partial=True
        )
        serilizer.is_valid(raise_exception=True)
        if request.method == 'PATCH':
            serilizer.save()
        return Response(serilizer.data, status=status.HTTP_200_OK)
