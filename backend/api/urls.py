from django.urls import path
from api.views import hello_django, hello_django_drf, execute_command, connect_user

urlpatterns = [
    path('hello-django/', hello_django, name='hello_django'),
    path('hello-django-drf/', hello_django_drf, name='hello_django'),
    path('connect-user/', connect_user, name='connect_user'),
    path('input-command/', execute_command, name='execute_command'),
]