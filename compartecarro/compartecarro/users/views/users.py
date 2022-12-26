# DRF
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Serializers
from compartecarro.users.serializers import (
    UserLoginSerializer,
    UserModelSerializer
)

class UserLoginAPIView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()

        data = {
            'user': UserModelSerializer(user).data,
            'token': token
        }

        return Response(data, status=status.HTTP_200_OK)