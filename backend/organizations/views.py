from rest_framework import generics, permissions
from .models import Organization, Membership
from .serializers import OrganizationSerializer, MembershipSerializer


class OrganizationListCreateView(generics.ListCreateAPIView):
    serializer_class = OrganizationSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Organization.objects.filter(
            memberships__user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save()


class OrganizationDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrganizationSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Organization.objects.filter(
            memberships__user=self.request.user
        )


class MembershipListView(generics.ListAPIView):
    serializer_class = MembershipSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Membership.objects.filter(
            organization__id=self.kwargs['org_id'],
            organization__memberships__user=self.request.user
        )