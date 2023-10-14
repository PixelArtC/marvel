from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('deposit/', views.deposit, name='deposit'),
    path('marketplace/', views.marketplace, name='marketplace'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
]
