from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItemList, ShipmentList, ShipmentDetail, TrackingFormAPIView, GetTrackingFormAPIView, TrackingDetailAPIView

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'items', ItemList)
router.register(r'shipment', ShipmentList)

urlpatterns = [
    path('', include(router.urls)),
    path('shipment/<str:tracking_id>/', ShipmentDetail.as_view(), name='shipment_detail'),
    path('item-list/', ItemList.as_view({'get': 'list', 'post': 'create'}), name='item-list'),
    path('shipments/', ShipmentList.as_view({'get': 'list', 'post': 'create'}), name='shipment-list'),
		# tracking
    path('posttracking/', TrackingFormAPIView.as_view(), name='posttracking'),
    path('gettracking/', GetTrackingFormAPIView.as_view(), name='gettracking'),
    path('tracking/<int:pk>/', TrackingDetailAPIView.as_view(), name='tracking-detail'),
]