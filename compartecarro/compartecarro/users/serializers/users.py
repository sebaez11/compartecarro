# Django
from django.contrib.auth import authenticate, password_validation
from django.core.validators import RegexValidator
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings

# DRF
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator
from rest_framework import serializers

# Serializers
from .profiles import ProfileModelSerializer

# Models
from compartecarro.users.models import User, Profile

# Utilities
from datetime import timedelta
import jwt


class UserModelSerializer(serializers.ModelSerializer):

    profile = ProfileModelSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'profile'
        )

class UserLoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        """ Validate User Credentials """

        user = authenticate(username=data["email"], password=data["password"])
        if not user:
            raise serializers.ValidationError({"credentials_error":"Bad Credentials"})

        if not user.is_verified:
            raise serializers.ValidationError({"verified_error":"User is not verified yet"})

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
        user = User.objects.create_user(**data, is_verified=False, is_cliente=True)
        Profile.objects.create(user=user)
        self.send_confirmation_email(user)
        return user

    def send_confirmation_email(self, user):
        """Send an email to allow users to confirm accounts."""

        verification_token = self.generate_verification_token(user)
        
        subject = f'Welcome @{user.username}! Verify your account to start using Comparte Carro'
        from_email = 'Comparte Carro <noreply@compartecarro.com>'
        content = render_to_string(
            'emails/users/account_verification.html',
            {
                'token': verification_token,
                'user': user
            }
        )
        msg = EmailMultiAlternatives(subject, content, from_email, [user.email])
        msg.attach_alternative(content, "text/html")
        msg.send()

    def generate_verification_token(self, user):
        """Create a JWT Token that the user can use to verify its account."""

        exp_date = timezone.now() + timedelta(days=3)
        payload = {
            'user': user.username,
            'exp': int(exp_date.timestamp()),
            'type': 'email_confirmation'
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        return token

    
class AccountVerificationSerializer(serializers.Serializer):

    token = serializers.CharField()

    def validate_token(self, data):
        try:
            payload = jwt.decode(data, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError('Verification link has expired.')
        except jwt.PyJWTError:
            raise serializers.ValidationError('Invalid token')
        if payload['type'] != 'email_confirmation':
            raise serializers.ValidationError('Invalid token')
        
        self.context['payload'] = payload

        return data

    def save(self):
        payload = self.context['payload']
        user = User.objects.get(username=payload['user'])
        user.is_verified = True
        user.save()