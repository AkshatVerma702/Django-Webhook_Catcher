from . import views
from django.urls import path

urlpatterns = [
    path('request/', views.catch, name='catchRequests'),
    path('allrequests/', views.viewRequests, name="getAllRequests"),
    path("<int:target_id>/", views.getRequest, name="getRequest"),
    path("all_requests/", views.delete_all_requests,name="delete_all"),
]