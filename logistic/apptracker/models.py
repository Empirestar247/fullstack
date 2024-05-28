from django.db import models

# Create your models here.
from django.db import models
from datetime import datetime
import string
import random
from django.utils import timezone
import pytz
from datetime import datetime, timedelta
from django.utils import timezone

class Items(models.Model):
    item_id = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=50)
    item_price = models.IntegerField()
    quantity = models.IntegerField()
    trackingid = models.CharField(max_length=10, null=True, default='')
    Date = models.DateField(null=False, default=timezone.now)
    Time = models.TimeField(null=False, default=timezone.now)
    date_created = models.DateTimeField(auto_now_add=True)  

    def __str__(self) -> str:
        return self.item_name + str(self.item_price) + str(self.quantity) + str(self.trackingid)

def generate_tracking_id():
    characters = string.ascii_letters + string.digits 
    tracking_id = ''.join(random.choice(characters) for i in range(8))
    return tracking_id

class Shipment(models.Model):
    STATUS_CHOICES = [
        ('processing', 'Processing'),
        ('on_the_way', 'On the way'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('returned', 'Returned'),
        ('delayed', 'Delayed'),
    ]
    order_id = models.AutoField(primary_key=True)
    item_id = models.ForeignKey(Items, on_delete=models.CASCADE)
    Date_of_Departure = models.DateField(null=False, default=timezone.now)
    expected_delivery = models.DateTimeField(default=timezone.now() + timedelta(days=7))
    Sender_Name = models.CharField(max_length=400, null=False)
    Sender_Origin = models.CharField(max_length=200, null=False)
    From = models.CharField(max_length=400, null=False)
    To = models.CharField(max_length=400, null=False)
    quantity = models.IntegerField()
    customer = models.CharField(max_length=50)
    shipment_address = models.CharField(max_length=500)
    country = models.CharField(max_length=50)
    location = models.CharField(max_length=200, blank=True)
    order_date = models.DateTimeField(auto_now_add=True)  # Use auto_now_add for created timestamp
    Reciver_Phone = models.CharField(max_length=200, null=False)
    Item_Description = models.CharField(max_length=200, null=False)
    Weight_And_Dimension = models.TextField(blank=True)
    delicate_item = models.BooleanField()
    fast_delivery = models.BooleanField()
    shipping_charge = models.IntegerField(blank=True, editable=False, default=0)
    tracking_id = models.CharField(max_length=10, blank=True, editable=False, default=generate_tracking_id)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='processing',
    )

    def __str__(self):
        return self.tracking_id

class Tracking(models.Model):
    tracking_id = models.CharField(max_length=10, primary_key=True)
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=Shipment.STATUS_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)  # Use auto_now_add for created timestamp

    def __str__(self):
        return self.tracking_id