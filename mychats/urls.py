from django.urls import path
from . import views


urlpatterns = [
    path('user/chat/<str:username>/', views.chat_views_user, name='user_messages'),
]
