# Django
from django.core.validators import RegexValidator
from django.contrib.auth import authenticate, password_validation

# DRF
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator
from rest_framework import serializers

# Models
from compartecarro.users.models import User, Profile

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


class UserSignupSerializer(serializers.Serializer):

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    username = serializers.CharField(
        min_length=4,
        max_length=20,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message='Phone number must be entered in the format: +9999999999. Up to 15 digits allowed.'
    )
    phone_number = serializers.CharField(
        validators=[phone_regex]
    )

    password = serializers.CharField(min_length=8, max_length=64)
    password_confirmation = serializers.CharField(min_length=8, max_length=64)

    first_name = serializers.CharField(min_length=2, max_length=30)
    last_name = serializers.CharField(min_length=2, max_length=30)

    def validate(self, data):
        
        password = data["password"]
        password_confirmation = data["password_confirmation"]

        password_validation.validate_password(password)

        if password != password_confirmation:
            raise serializers.ValidationError({'passwords': 'Passwords do not match'})
        
        return data

    def create(self, data):

        data.pop("password_confirmation")
        user = User.objects.create_user(**data)
        profile = Profile.objects.create(user=user)

        return user