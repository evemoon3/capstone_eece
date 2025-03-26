from django.urls import path
from . import views

urlpatterns = [
    path('stuff/', views.members, name='stuff'),
]