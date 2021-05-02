from rest_framework.exceptions import APIException
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .authentication import TemporaryTokenAuth
from .my_permissions import IsPerformerOrAdmin, IsOwnerOrAdmin
from .serializers import *
from desk.models import TaskModel


class ShowCardsAPIView(ListAPIView):
    authentication_classes = [TemporaryTokenAuth]
    queryset = TaskModel.objects.all()
    serializer_class = CardsListSerializer


class CreateCardAPIView(CreateAPIView):
    authentication_classes = [TemporaryTokenAuth]
    serializer_class = CardSerializer

    def perform_create(self, serializer):
        try:
            performer = serializer.validated_data['performer']
            if not performer or performer == self.request.user:
                serializer.save(owner=self.request.user)
            else:
                raise APIException("You can assign only yourself as a performer")
        except KeyError:
            serializer.save(owner=self.request.user)


class RaiseStatusAPIView(UpdateAPIView):
    authentication_classes = [TemporaryTokenAuth]
    permission_classes = [IsAuthenticated, IsPerformerOrAdmin]
    queryset = TaskModel.objects.all()
    serializer_class = CardUpdateStatusSerializer

    def perform_update(self, serializer):
        card = self.get_object()
        user = self.request.user
        if card.status < 4 and not user.is_superuser or 3 < card.status < 5 and user.is_superuser:
            serializer.save(status=card.status + 1)
        else:
            raise APIException("You cannot raise the card's status higher")


class OmitStatusAPIView(UpdateAPIView):
    authentication_classes = [TemporaryTokenAuth]
    permission_classes = [IsAuthenticated, IsPerformerOrAdmin]
    queryset = TaskModel.objects.all()
    serializer_class = CardUpdateStatusSerializer

    def perform_update(self, serializer):
        card = self.get_object()
        user = self.request.user
        if 5 > card.status >= 3 and not user.is_superuser or card.status > 4 and user.is_superuser:
            serializer.save(status=card.status-1)
        else:
            raise APIException("You cannot omit the card's status below")


class DeleteCardAPIView(DestroyAPIView):
    authentication_classes = [TemporaryTokenAuth]
    permission_classes = [IsAdminUser]
    queryset = TaskModel.objects.all()


class UpdateCardAPIView(UpdateAPIView):
    authentication_classes = [TemporaryTokenAuth]
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    queryset = TaskModel.objects.all()
    serializer_class = CardUpdateSerializer

    def perform_update(self, serializer):
        user = self.request.user
        try:
            performer = serializer.validated_data['performer']
            if not performer or performer == user or user.is_superuser:
                if not performer or not performer.is_superuser:
                    serializer.save()
                else:
                    raise APIException("Admin cannot assign himself as a performer")
            else:
                raise APIException("You can assign only yourself as a performer")
        except KeyError:
            serializer.save()
