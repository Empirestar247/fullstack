from django.shortcuts import render
from django.http import HttpResponse
from .models import Tracking
# Create your views here.
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from django.utils.timezone import get_current_timezone
import pytz
from .models import Items, Shipment, Tracking
from .serializers import ItemSerializer, ShipmentSerializer, TrackingSerializer
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView


def display_tracking_info(request, tracking_id):
    try:
        tracking = Tracking.objects.get(tracking_id=tracking_id)
        return HttpResponse(tracking)
    except Tracking.DoesNotExist:
        return HttpResponse('Tracking information not found', status=404)


class ShipmentDetail(APIView):
    """
    Retrieve a shipment instance.
    """
    def get(self, request, tracking_id, format=None):
        shipment = get_object_or_404(Shipment, tracking_id=tracking_id)
        serializer = ShipmentSerializer(shipment)
        return Response(serializer.data)

class ItemList(viewsets.ModelViewSet):
    queryset = Items.objects.all()
    serializer_class = ItemSerializer

class ShipmentList(viewsets.ModelViewSet):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer

    def create(self, request):
        print(request.data)
        item_id = request.data["item_id"]
        quantity = int(request.data["quantity"])
        shipment_data=ShipmentSerializer(data=request.data)
        if shipment_data.is_valid():
            shipment_data.save()
        order_list = Shipment.objects.values_list('order_id', flat=True)
        order_id = order_list[len(order_list)-1]
        tracking_id = Shipment.objects.get(order_id=order_id).tracking_id
        _shipment = Shipment.objects.get(order_id=order_id)
        try:
            if request.data["fast_delivery"]:
                _shipment.expected_delivery = timezone.now() + timedelta(hours=24)
                _shipment.shipping_charge = 50
            else:
                _shipment.expected_delivery = timezone.now() + timedelta(hours=240)
                _shipment.shipping_charge = 50
        except KeyError:
            _shipment.expected_delivery = timezone.now() + timedelta(hours=240)
            _shipment.shipping_charge = 50

        # Handle new_field
        _shipment.new_field = request.data.get('new_field', 'default_value')
        
        _shipment.save()
        item = Items.objects.get(item_id=item_id)
        if item.quantity < quantity:
            return Response("Out of stock", status=status.HTTP_400_BAD_REQUEST)
        else:
            item.quantity = item.quantity-quantity  # change field
            item.save()
            return Response({"Order Id": order_id,
                            "Tracking Id": tracking_id,
                            "expected_delivery":_shipment.expected_delivery,
                            "shipping_charge": _shipment.shipping_charge,
                            "Total Cost(including shipping charge)": (quantity*int(item.item_price))
                                                                        + _shipment.shipping_charge
            }, status=status.HTTP_200_OK)

class TrackingFormAPIView(APIView):
    def post(self, request, format=None):
        serializer = TrackingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetTrackingFormAPIView(ListAPIView):
    queryset = Tracking.objects.all()
    serializer_class = TrackingSerializer

class TrackingDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Tracking.objects.all()
    serializer_class = TrackingSerializer


from django.http import JsonResponse, Http404
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Shipment
import json

@method_decorator(csrf_exempt, name='dispatch')
class PostTrackingView(View):
    def post(self, request):
        data = json.loads(request.body)
        tracking_id = data.get('trackingId', None)
        if not tracking_id:
            return JsonResponse({"message": "Tracking ID is required"}, status=400)
        try:
            shipment = Shipment.objects.get(tracking_id=tracking_id)
            return JsonResponse({
                "status": shipment.status,
                "location": shipment.location,
                "expectedDelivery": shipment.expected_delivery
            })
        except ObjectDoesNotExist:
            return JsonResponse({"message": "Shipment not found"}, status=404)

    def get(self, request):
        return JsonResponse({"message": "GET request received"})


