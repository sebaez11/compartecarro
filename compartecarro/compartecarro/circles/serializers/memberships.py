# DRF
from rest_framework import serializers

# Models
from compartecarro.circles.models import Membership, Invitation

#Serializers
from compartecarro.users.serializers import UserModelSerializer

# Utilities
from django.utils import timezone


class MembershipModelSerializer(serializers.ModelSerializer):

    user = UserModelSerializer(read_only=True)
    invited_by = serializers.StringRelatedField()
    joined_at = serializers.DateTimeField(source='created_at', read_only=True)

    class Meta:
        model = Membership
        fields = (
            'user',
            'is_admin', 'is_active',
            'used_invitations', 'remaining_invitations',
            'invited_by',
            'rides_taken', 'rides_offered',
            'joined_at'
        )
        read_only_fields = (
            'user',
            'used_invitations',
            'invited_by',
            'rides_taken', 'rides_offered'
        )


class AddMemberSerializer(serializers.Serializer):

    invitation_code = serializers.CharField(min_length=8)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_user(self, data):
        circle = self.context['circle']
        user = data
        membership = Membership.objects.filter(circle=circle, user=user)
        if membership.exists():
            raise serializers.ValidationError(f'User is already member of {circle.slug_name}')
        
    def validate_invitation_code(self, data):
        try:
            invitation = Invitation.objects.get(
                code=data,
                circle=self.context['circle'],
                used=False
            )
        except Invitation.DoesNotExist:
            raise serializers.ValidationError('Invalid invitation code.')
        self.context['invitation'] = invitation

        return data

    def validate(self, data):
        circle = self.context['circle']
        if circle.is_limited and circle.members.count() >= circle.members_limit:
            raise serializers.ValidationError('Circle has reached its member limit :(')
        return data

    def create(self, data):
        circle = self.context['circle']
        invitation = self.context['invitation']
        request = self.context['request']
        user = request.user

        now = timezone.now()

        member = Membership.objects.create(
            user=user,
            profile=user.profile,
            circle=circle,
            invited_by=invitation.issued_by
        )

        invitation.used_by = user
        invitation.used = True
        invitation.used_at = now
        invitation.save()

        issuer = Membership.objects.get(user=invitation.issued_by, circle=circle)
        issuer.used_invitations += 1
        issuer.remaining_invitations -= 1
        issuer.save()

        return member