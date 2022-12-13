# REST Framework
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Models
from compartecarro.circles.models import Circle

# Serializers
from compartecarro.circles.serializers import (
    CircleSerializer,
    CreateCircleSerializer
)

@api_view(['GET'])
def list_circles(request):
    """List all circles with 'is_public' property equals True"""

    public_circles = Circle.objects.filter(is_public=True)
    serializer = CircleSerializer(public_circles, many=True)
    
    return Response(serializer.data)

@api_view(['POST'])
def create_circle(request):
    
    serializer = CreateCircleSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    circle = serializer.save()
    return Response(CircleSerializer(circle).data)