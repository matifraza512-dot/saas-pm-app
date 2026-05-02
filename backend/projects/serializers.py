from rest_framework import serializers
from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)
    task_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ('id', 'organization', 'name', 'description',
                  'status', 'created_by', 'task_count', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_by', 'created_at', 'updated_at')

    def get_task_count(self, obj):
        return obj.tasks.count()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)