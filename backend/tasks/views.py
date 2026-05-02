from rest_framework import generics, permissions
from .models import Task
from .serializers import TaskSerializer
from organizations.models import Membership


class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user_orgs = Membership.objects.filter(
            user=self.request.user
        ).values_list('organization_id', flat=True)
        qs = Task.objects.filter(project__organization__in=user_orgs)
        project_id = self.request.query_params.get('project')
        if project_id:
            qs = qs.filter(project__id=project_id)
        return qs


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user_orgs = Membership.objects.filter(
            user=self.request.user
        ).values_list('organization_id', flat=True)
        return Task.objects.filter(project__organization__in=user_orgs)