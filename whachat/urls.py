from django.urls import path
from . import views


urlpatterns = [
    path('user/chat/<str:username>/', views.users_chattings, name='user_chat')
]
