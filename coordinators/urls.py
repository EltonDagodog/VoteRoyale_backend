from django.urls import path
from .views import coordinator_register, coordinator_login

urlpatterns = [
    path('register/', coordinator_register, name='coordinator_register'),
    path('login/', coordinator_login, name='coordinator_login'),
]