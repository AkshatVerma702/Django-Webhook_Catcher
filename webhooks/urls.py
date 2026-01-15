from . import views
from django.urls import path

urlpatterns = [
    path('request/', views.testing)
]