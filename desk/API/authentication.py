from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from django.utils import timezone

from Trello.settings import AUTO_LOGOUT_TIME
from desk.models import TemporaryTokenModel


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
