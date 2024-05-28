from django.urls import path
from .views import delete_tracking_info, update_tracking_id, display_tracking_info, register
from .views import search


urlpatterns = [
    path('delete_tracking_info/', delete_tracking_info, name='delete_tracking_info'),
    path('update_tracking_id/', update_tracking_id, name='update_tracking_id'),
    path('display_tracking_info/', display_tracking_info, name='display_tracking_info'),
    path('register/', register, name='register'),
		path('search/', search, name='search'),    
]