from django.db import models
from django.contrib.auth.models import User

class Tracking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tracking_id = models.CharField(max_length=200)

    def __str__(self):
        return self.tracking_id

