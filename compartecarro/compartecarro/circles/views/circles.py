# DRF
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

# Models
from compartecarro.circles.models import Circle, Membership

# Serializers
from compartecarro.circles.serializers import CircleModelSerializer


class CircleModelViewSet(viewsets.ModelViewSet):

    serializer_class = CircleModelSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        
        queryset = Circle.objects.all()
        if self.action == 'list':
            return queryset.filter(is_public=True)
        return queryset

    def perform_create(self, serializer):

        circle = serializer.save()
        user = self.request.user
        profile = user.profile
        Membership.objects.create(
            user=user,
            profile=profile,
            circle=circle,
            is_admin=True,
            remaining_invitations=10
        )