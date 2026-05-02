from rest_framework import generics, permissions
from .models import Project
from .serializers import ProjectSerializer
from organizations.models import Membership


class ProjectListCreateView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user_orgs = Membership.objects.filter(
            user=self.request.user
        ).values_list('organization_id', flat=True)
        return Project.objects.filter(organization__in=user_orgs)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user_orgs = Membership.objects.filter(
            user=self.request.user
        ).values_list('organization_id', flat=True)
        return Project.objects.filter(organization__in=user_orgs)