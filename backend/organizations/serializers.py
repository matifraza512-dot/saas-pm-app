from rest_framework import serializers
from .models import Organization, Membership
from accounts.serializers import UserSerializer


class OrganizationSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    member_count = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = ('id', 'name', 'slug', 'owner', 'member_count', 'created_at')
        read_only_fields = ('id', 'owner', 'created_at')

    def get_member_count(self, obj):
        return obj.memberships.count()

    def create(self, validated_data):
        user = self.context['request'].user
        org = Organization.objects.create(owner=user, **validated_data)
        Membership.objects.create(user=user, organization=org, role='admin')
        return org


class MembershipSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Membership
        fields = ('id', 'user', 'role', 'joined_at')
        read_only_fields = ('id', 'user', 'joined_at')