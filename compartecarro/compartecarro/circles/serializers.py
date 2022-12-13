# DRF
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

# Models
from compartecarro.circles.models import Circle


class CircleSerializer(serializers.Serializer):

    name = serializers.CharField()
    slug_name = serializers.SlugField()
    rides_offered = serializers.IntegerField()
    rides_taken = serializers.IntegerField()


class CreateCircleSerializer(serializers.Serializer):

    name = serializers.CharField(max_length=140)
    slug_name = serializers.SlugField(
        max_length=40,
        validators=[
            UniqueValidator(queryset=Circle.objects.all()),
        ]
    )
    about = serializers.CharField(
        max_length=255,
        required=False
    )

    def create(self, validated_data):
        return Circle.objects.create(**validated_data)