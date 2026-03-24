from . import views
from django.urls import path

urlpatterns = [
    path('catch/request/', views.generateToken, name='generateToken'),
    path('view/allrequests/', views.viewRequests, name="getAllRequests"),
    path("delete_all/", views.delete_all_requests,name="delete_all"),
    path("request/<int:target_id>/", views.getRequest, name="getRequest"),
    path('webhook/<uuid:token>/', views.catchRequest, name='catchRequest'),
    path('api/requests', views.updateView, name='updateView')
]