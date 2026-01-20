from django.urls import path
from . import views

urlpatterns = [
    path('grade/', views.upload_and_grade, name='grade_submission'),
]