# DRF
from rest_framework import serializers

# Models
from compartecarro.rides.models import Ride
from compartecarro.circles.models import Membership

# Utilities
from django.utils import timezone
from datetime import timedelta

class CreateRideSerializer(serializers.ModelSerializer):

    offered_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    available_seats = serializers.IntegerField(min_value=1, max_value=15)

    class Meta:

        model = Ride
        exclude = ('offered_in', 'passengers', 'rating', 'is_active')

    def validate_departure_date(self, data):

        min_date = timezone.now() + timedelta(minutes=10)

        if data < min_date:
            raise serializers.ValidationError(
                'Departure time must be at least pass the next 20 minutes window.'
            )
        
        return data

    def validate(self, data):

        if self.context['request'].user != data['offered_by']:
            raise serializers.ValidationError('Rides offered on behalf of others are not allowed.')

        user = data['offered_by']
        circle = self.context['circle']

        try:
            membership = Membership.objects.filter(
                user=user, 
                circle=circle, 
                is_active=True
            )
        except Membership.DoesNotExist:
            raise serializers.ValidationError('User is not an active member of the circle.')
        
        if data['arrival_date'] <= data['departure_date']:
            raise serializers.ValidationError('Departure date must happen after arrival date.')

        self.context['membership'] = membership

        return data

    def create(self, data):

        circle = self.context['circle']
        ride = Ride.objects.create(**data, offered_in=circle)

        # Circle
        circle.rides_offered += 1
        circle.save()

        # Membership
        membership = self.context['membership']
        membership.rides_offered += 1
        membership.save()

        # Profile
        profile = data['offered_by'].profile
        profile.rides_offered += 1
        profile.save()

        return ride