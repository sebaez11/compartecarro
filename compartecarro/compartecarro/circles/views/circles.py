# DRF
from rest_framework import viewsets, mixins

# Models
from compartecarro.circles.models import Circle, Membership

# Serializers
from compartecarro.circles.serializers import CircleModelSerializer

# Permissions
from rest_framework.permissions import IsAuthenticated
from compartecarro.circles.permissions import IsCircleAdmin


class CircleModelViewSet(mixins.CreateModelMixin, 
                         mixins.RetrieveModelMixin, 
                         mixins.UpdateModelMixin, 
                         mixins.ListModelMixin, 
                         viewsets.GenericViewSet):

    serializer_class = CircleModelSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        
        queryset = Circle.objects.all()
        if self.action == 'list':
            return queryset.filter(is_public=True)
        return queryset

    def get_permissions(self):
        permissions = [IsAuthenticated]
        if self.action in ['update', 'partial_update']:
            permissions.append(IsCircleAdmin)

        return [permission() for permission in permissions]

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