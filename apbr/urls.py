from django.urls import path
from extras.views import ObjectChangeLogView
from .models import Apbr

from .views import (
    ApbrListView, ApbrView, ApbrBulkDeleteView, ApbrEditView, ApbrBulkEditView,
    ApbrDeleteView
)

urlpatterns = [
    path('apbr/', ApbrListView.as_view(), name='apbr_list'),
    path('apbr/add/', ApbrEditView.as_view(), name='apbr_add'),
    path('apbr/edit/', ApbrBulkEditView.as_view(), name='apbr_bulk_edit'),
    path('apbr/delete/', ApbrBulkDeleteView.as_view(), name='apbr_bulk_delete'),
    path('apbr/<int:pk>/', ApbrView.as_view(), name='apbr'),
    path('apbr/<int:pk>/edit/', ApbrEditView.as_view(), name='apbr_edit'),
    path('apbr/<int:pk>/delete/', ApbrDeleteView.as_view(), name='apbr_delete'),
    path('apbr/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='apbr_changelog', kwargs={'model': Apbr}),
]