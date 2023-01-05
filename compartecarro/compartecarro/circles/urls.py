# Django
from django.urls import path, include

# DRF
from rest_framework.routers import DefaultRouter

# Views
from compartecarro.circles.views import CircleModelViewSet, MembershipViewSet

router = DefaultRouter()

router.register(
    prefix='',
    viewset=CircleModelViewSet,
    basename='circles'
)

router.register(
    prefix=r'(?P<slug_name>[-a-zA-Z0-9_]+)/members',
    viewset=MembershipViewSet,
    basename='membership'
)

urlpatterns = [
    path(
        '',
        include(router.urls),
    )
]

