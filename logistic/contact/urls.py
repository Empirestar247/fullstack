from django.urls import path
from . import views

urlpatterns = [
    path('postcontact/', views.get_contact_api_view, name='postcontact'),
    path('getcontact/', views.get_contact_api_views, name='getcontact'),
    
]