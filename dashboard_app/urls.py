from django.urls import path
from .views import dashboard_view, upload_document

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('upload/', upload_document, name='upload_document'),
]
