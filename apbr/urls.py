from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.RandomApbrProfileView.as_view(), name='random_profile'),
    path('random/', views.RandomApbrProfileView.as_view(), name='random_profile'),
]
