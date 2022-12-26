# Django
from django.contrib.auth import authenticate

# DRF
from rest_framework.authtoken.models import Token
from rest_framework import serializers

# Models
from compartecarro.users.models import User

class UserModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number'
        )

class UserLoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        """ Validate User Credentials """

        user = authenticate(username=data["email"], password=data["password"])
        if not user:
            raise serializers.ValidationError("Bad Credentials")

        self.context['user'] = user
        
        return data

    def create(self, data):
        user = self.context['user']
        token, created = Token.objects.get_or_create(user=user)

        return user, token.key