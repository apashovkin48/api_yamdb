



from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework.decorators import  api_view
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (
    ReviewSerializer,
    CommentSerializer,
    ApiSignupSerializer,
    ApiTokenSerializer
)
from reviews.models import Review


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(review=review)
        

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
