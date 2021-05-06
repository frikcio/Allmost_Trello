from rest_framework import serializers
from desk.models import TaskModel, TrelloUser


class RegisterUserSerializer(serializers.ModelSerializer):
    re_password = serializers.CharField(max_length=120)

    class Meta:
        model = TrelloUser
        fields = ['username', 'password', 're_password']

    def validate(self, attrs):
        if attrs['password'] == attrs['re_password']:
            return attrs


class CardsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskModel
        exclude = ['screenshot']


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskModel
        fields = ['title', 'text', 'performer']


class CardUpdateStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskModel
        fields = []


class CardUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskModel
        fields = ['text', 'performer']


class GetCardsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskModel
        exclude = ['screenshot', 'created', 'status']
