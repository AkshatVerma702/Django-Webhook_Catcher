from . import views
from django.urls import path

urlpatterns = [
    path('request/', views.catch),
    path('allrequests/', views.viewRequests),
    path("<int:target_id>/", views.getRequest, name="getRequest")
]