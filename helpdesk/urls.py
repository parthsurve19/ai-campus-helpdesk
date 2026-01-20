from django.urls import path
from .views import campus_helpdesk

urlpatterns = [
    path("", campus_helpdesk, name="campus_helpdesk"),
]
