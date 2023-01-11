# Django
from django.urls import path, include

# DRF
from rest_framework.routers import DefaultRouter

# Views
from compartecarro.rides.views import RideViewSet

router = DefaultRouter()

router.register(
    prefix=r'(?P<slug_name>[-a-zA-Z0-9_]+)/rides',
    viewset=RideViewSet,
    basename='rides'
)

urlpatterns = [
    path(
        '',
        include(router.urls),
    )
]

