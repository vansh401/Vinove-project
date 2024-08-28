from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='start_tracking'),
]
