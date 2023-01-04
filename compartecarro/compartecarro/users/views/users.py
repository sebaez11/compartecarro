# DRF
from rest_framework import viewsets, mixins
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
from compartecarro.circles.serializers import CircleModelSerializer

# Permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from compartecarro.users.permissions import IsAccountOwner

# Models
from compartecarro.users.models import User
from compartecarro.circles.models import Circle


class UserViewSet(mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):

    queryset = User.objects.filter(is_active=True, is_client=True)
    serializer_class = UserModelSerializer
    lookup_field = 'username'

    def get_permissions(self):
        if self.action in ['signup', 'login', 'verify']:
            permissions = [AllowAny]
        elif self.action == 'retrieve':
            permissions = [IsAuthenticated, IsAccountOwner]
        else:
            permissions = [IsAuthenticated]
        
        return [permission() for permission in permissions]

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

    def retrieve(self, request, *args, **kwargs):
        response = super(UserViewSet, self).retrieve(request, *args, **kwargs)
        circles = Circle.objects.filter(
            members=request.user,
            membership__is_active=True
        )
        data = {
            'user': response.data,
            'circles': CircleModelSerializer(circles, many=True).data
        }

        response.data = data
        return response