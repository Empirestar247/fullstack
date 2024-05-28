from django.contrib import admin # type: ignore


# Register your models here.
from .models import contact


admin.site.register(contact)