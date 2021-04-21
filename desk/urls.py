from django.urls import path

from desk.views import Register, Login, Logout, ProfileView, HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
]
