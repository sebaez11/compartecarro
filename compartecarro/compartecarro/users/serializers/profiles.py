# DRF
from rest_framework import serializers

# Models
from compartecarro.users.models import Profile


class ProfileModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = (
            'picture',
            'biography',
            'rides_taken',
            'rides_offered',
            'reputation'
        )

        read_only_fields = (
            'rides_taken',
            'rides_offered',
            'reputation'
        )