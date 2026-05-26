from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/upload/', views.upload_design, name='upload_design'),
    path('api/status/<int:job_id>/', views.check_status, name='check_status'),
]
