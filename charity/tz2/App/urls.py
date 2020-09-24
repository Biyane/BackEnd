from django.urls import path
from . import views
from rest_framework.authtoken import views as jwtview

urlpatterns = [
    path('', views.get_or_post_list_of_users, name='user list or create user'),
    # path('list/', views.MedicinesList.as_view(), name='medicines list'),
    # path('test/', views.TestUserApi.as_view(), name='test'),
    path('login/', views.LoginView.as_view(), name='login'),
    # path('hello/', views.UserApi.as_view(), name='hello'),
    path('api-auth-token/', views.CustomAuthToken.as_view(), name='api-auth-token'),
    path('list/', views.MedicinesListApi.as_view(), name='da fuk'),
    path('logout/', views.LogOutView.as_view(), name='logout'),
]


