# Django
from django.urls import path

# Views
from compartecarro.users.views import (
    UserLoginAPIView,
    UserSignUpAPIView,
    AccountVerificationAPIView
)

urlpatterns = [

    path(
        route='login/',
        view=UserLoginAPIView.as_view(),
        name='login'
    ),
    path(
        route='signup/',
        view=UserSignUpAPIView.as_view(),
        name='signup'
    ),
    path(
        route='verify/',
        view=AccountVerificationAPIView.as_view(),
        name='verify'
    ),

]