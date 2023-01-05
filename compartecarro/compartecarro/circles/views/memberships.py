# DRF
from rest_framework import mixins, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response

# Models
from compartecarro.circles.models import Circle, Membership, Invitation

# Permissions
from rest_framework.permissions import IsAuthenticated
from compartecarro.circles.permissions import IsActiveCircleMember

# Serializers
from compartecarro.circles.serializers import MembershipModelSerializer


class MembershipViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):

    serializer_class = MembershipModelSerializer

    def dispatch(self, request, *args, **kwargs):
        slug_name = kwargs['slug_name']
        self.circle = get_object_or_404(Circle, slug_name=slug_name)
        return super(MembershipViewSet, self).dispatch(request, *args, **kwargs)

    def get_permissions(self):

        permissions = [IsAuthenticated, IsActiveCircleMember]
        return [permission() for permission in permissions]

    def get_queryset(self):
        return Membership.objects.filter(circle=self.circle, is_active=True)

    def get_object(self):

        return get_object_or_404(
            Membership,
            user__username=self.kwargs['pk'],
            circle=self.circle,
            is_active=True
        )
    
    def perform_destroy(self, instance):

        instance.is_active = False
        instance.save()

    @action(detail=True, methods=['GET'])
    def invitations(self, request, *args, **kwargs):

        member = self.get_object()
        invited_members = Membership.objects.filter(
            circle=self.circle,
            invited_by=request.user,
            is_active=True
        )

        unused_invitations = Invitation.objects.filter(
            circle=self.circle,
            issued_by=request.user,
            used=False
        ).values_list('code')
        diff = member.remaining_invitations - len(unused_invitations)

        invitations = [x[0] for x in unused_invitations]

        for i in range(0, diff):
            invitations.append(
                Invitation.objects.create(
                    issued_by=request.user,
                    circle=self.circle
                ).code
            )

        data = {
            'used_invitations': MembershipModelSerializer(
                invited_members, many=True
            ).data,
            'invitations': invitations
        }

        return Response(data)