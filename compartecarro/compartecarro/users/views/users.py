# DRF
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

# Serializers
from compartecarro.users.serializers import (
    UserLoginSerializer,
    UserSignupSerializer,
    UserModelSerializer,
    AccountVerificationSerializer
)


class UserViewSet(viewsets.GenericViewSet):

    @action(detail=False, methods=['POST'])
    def login(self, request):    
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': UserModelSerializer(user).data,
            'token': token
        }
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'])
    def signup(self, request):
        serializer = UserSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = {
            "user": UserModelSerializer(user).data
        }
        return Response(data)

    @action(detail=False, methods=['POST'])
    def verify(self, request):
        serializer = AccountVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            'message': 'Congratulations, now go share some rides!'
        }
        return Response(data)