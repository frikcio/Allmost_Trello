from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions, status
from rest_framework.exceptions import APIException
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from django.utils import timezone

from Trello.settings import AUTO_LOGOUT_TIME
from desk.API.serializers import RegisterUserSerializer
from desk.models import TemporaryTokenModel, TrelloUser


class RegisterUserAPIView(CreateAPIView):
    serializer_class = RegisterUserSerializer
    model = TrelloUser
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            TrelloUser.objects.create_user(username=username, password=password)
            return Response('You are register now)', status=status.HTTP_201_CREATED)
        except KeyError:
            raise APIException("The fields must be filled!!!")


class GetToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = TemporaryTokenModel.objects.get_or_create(user=user)
        if token.last_action and (timezone.now() - token.last_action).seconds > AUTO_LOGOUT_TIME * 60:
            token.delete()
            token = TemporaryTokenModel.objects.create(user=user)
        return Response({'token': token.key})


class TemporaryTokenAuth(TokenAuthentication):
    model = TemporaryTokenModel

    def authenticate(self, request):
        incoming_values = super().authenticate(request)
        if incoming_values:
            user, token = incoming_values
            if not user.is_superuser and token.last_action and (
                    timezone.now() - token.last_action).seconds > AUTO_LOGOUT_TIME * 60:
                msg = "Token's lifetime is over!"
                raise exceptions.AuthenticationFailed(msg)
            token.last_action = timezone.now()
            token.save()
            return user, token
