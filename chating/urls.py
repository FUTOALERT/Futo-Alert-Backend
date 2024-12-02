from django.urls import path
from . import views


urlpatterns = [
    path('user/<str:username>/', views.user_one_chat, name='user_chatting')
]
