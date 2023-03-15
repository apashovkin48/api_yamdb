from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework import status
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .permission import IsOnlyAdmin
from .serializers import ApiSignupSerializer, ApiTokenSerializer, \
    UserSerializer, MeSerilizer

User = get_user_model()


@api_view(['POST'])
def api_signup(request):
    serializer = ApiSignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data.get('email')
    username = serializer.validated_data.get('username')

    user = User.objects.filter(username=username).first()
    if user and user.email != email:
        return Response(
            {'email': 'неверный email'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = User.objects.filter(email=email).first()
    if user and user.username != username:
        return Response(
            {'username': 'неверный username'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user, created = User.objects.get_or_create(email=email, username=username)

    send_mail(
        subject='Тема письма',
        message=f'Код подтверждения: {user.confirmation_code}',
        from_email='FFFF@ffff.com',
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
        'Token': f'Bearer {str(RefreshToken.for_user(user).access_token)}'
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
