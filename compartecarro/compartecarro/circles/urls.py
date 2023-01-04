# Django
from django.urls import path, include

# DRF
from rest_framework.routers import DefaultRouter

# Views
from compartecarro.circles.views import CircleModelViewSet

router = DefaultRouter()

router.register(
    prefix='',
    viewset=CircleModelViewSet,
    basename='circles'
)

urlpatterns = [
    path(
        '',
        include(router.urls),
    )
]

