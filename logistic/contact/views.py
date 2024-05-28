from django.shortcuts import render 


# Create your views here.
from rest_framework.response import Response 
from rest_framework import status 
from .models import contact
from .serializers import ContactSerializers
from rest_framework.decorators import api_view 

@api_view(['POST'])
def get_contact_api_view(request, format=None):
    if request.method == "POST":
        serializer = ContactSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)	
	
@api_view(['GET'])
def get_contact_api_views(request, format=None):
  if request.method == "GET":
    contacts=contact.objects.all()
    serializers = ContactSerializers(contacts, many=True)
    return Response(serializers.data)
