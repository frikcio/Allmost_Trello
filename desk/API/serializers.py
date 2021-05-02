from rest_framework import serializers
from desk.models import TaskModel


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

