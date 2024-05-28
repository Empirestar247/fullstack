from rest_framework import fields, serializers
from .models import *


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Items
        fields = '__all__'

class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Shipment
        fields = '__all__'

class TrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tracking
        fields = '__all__'