# REST Framework
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Models
from compartecarro.circles.models import Circle

@api_view(['GET'])
def list_circles(request):
    """List all circles with 'is_public' property equals True"""

    public_circles = Circle.objects.filter(is_public=True)
    data = []

    for circle in public_circles:
        data.append({
            'name': circle.name,
            'slug_name': circle.slug_name,
            'rides_offered': circle.rides_offered,
            'rides_taken': circle.rides_taken,
        })
    
    return Response(data)

@api_view(['POST'])
def create_circle(request):
    
    name = request.data['name']
    slug_name = request.data['slug_name']
    about = request.data.get('about', '')
    
    circle = Circle.objects.create(name=name, slug_name=slug_name, about=about)

    data = {
        'name': circle.name,
        'slug_name': circle.slug_name,
        'about': circle.about,
        'rides_offered': circle.rides_offered,
    }

    return Response(data)