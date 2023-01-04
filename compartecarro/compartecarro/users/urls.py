# Django
from django.urls import path, include

# DRF
from rest_framework.routers import DefaultRouter

# Views
from compartecarro.users.views import UserViewSet

router = DefaultRouter()

router.register(
    prefix='',
    viewset=UserViewSet,
    basename='users'
)

urlpatterns = [

    path(
        route='',
        view=include(router.urls)
    )

]