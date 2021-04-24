from django.urls import path

from desk.views import *

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('project/add/', AddNewProjectView.as_view(), name='add_project'),
    path('projects/', ProjectsListView.as_view(), name='projects_list'),
    path('project/<str:project_name>/', HomeView.as_view(), name='project'),
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('task/create/', CreateCardView.as_view(), name='create_card'),
    path('task/change/perfomer/<int:pk>/', ChangePerfomerView.as_view(), name='change_perfomer'),
    path('card/status/rise/<int:pk>/', RiseStatusView.as_view(), name='rise'),
    path('card/status/omit/<int:pk>/', OmitStatusView.as_view(), name='omit'),
    path('card/delete/<int:pk>/', DeleteCardView.as_view(), name='delete'),
]
