from django.urls import path
from . import views

urlpatterns = [
    path('random/', views.RandomApbrProfileView.as_view(), name='random_profile'),
]
