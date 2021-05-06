from django.urls import path

from .authentication import GetToken, RegisterUserAPIView
from .resurses import *

urlpatterns = [
    path('register/', RegisterUserAPIView.as_view()),
    path('get/token/', GetToken.as_view()),
    path('card/list/', ShowCardsAPIView.as_view()),
    path('card/create/', CreateCardAPIView.as_view()),
    path('card/<int:pk>/status/raise/', RaiseStatusAPIView.as_view()),
    path('card/<int:pk>/status/omit/', OmitStatusAPIView.as_view()),
    path('card/<int:pk>/delete/', DeleteCardAPIView.as_view()),
    path('card/<int:pk>/update/', UpdateCardAPIView.as_view()),
    path('card/get/', GetCardSListAPIView.as_view()),
]
