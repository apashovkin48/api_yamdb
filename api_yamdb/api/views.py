from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import  api_view
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from .serializers import ApiSignupSerializer, ApiTokenSerializer
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


@api_view(['POST'])
def api_signup(request):
    serializer=ApiSignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email=serializer.validated_data.get('email')
    username=serializer.validated_data.get('username')
    user,created=User.objects.get_or_create(email=email, username=username)

    send_mail(
        subject='Тема письма',
        message=f'Код подтверждения: {user.confirmation_code}',
        from_email='FFFF@ffff.com',
        recipient_list=[user.email]
        )
    return Response(serializer.validated_data,status=status.HTTP_200_OK)


@api_view(['POST'])
def api_token(request):
    serializer=ApiTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    confirmation_code=serializer.validated_data.get('confirmation_code')
    username=serializer.validated_data.get('username')

    user=get_object_or_404(User,username=username)
    if confirmation_code != user.confirmation_code:
        return Response({'confirmation_code':"Отсутствует обязательное поле "
                                             "или оно некорректно"},
                        status=status.HTTP_400_BAD_REQUEST)
    return Response({
        'Token':f'Bearer {str(RefreshToken.for_user(user).access_token)}'
    })
