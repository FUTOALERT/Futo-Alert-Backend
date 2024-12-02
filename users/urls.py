from django.urls import path
from . import views


urlpatterns = [
    path('', views.user_login, name='user_login'),
    path('register/', views.user_registers, name='user_register'),
    path('account/update/<str:username>/', views.user_update_account, name='account_update'),
    path('account/user/settings/<str:username>/', views.get_user_settings, name='user_settings'),
    path('author/details/<str:username>/', views.author_profile_detail, name='author_profile'),
]
