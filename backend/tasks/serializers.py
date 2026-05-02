from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    assigned_to = serializers.StringRelatedField(read_only=True)
    assigned_to_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Task
        fields = ('id', 'project', 'title', 'description', 'status',
                  'priority', 'assigned_to', 'assigned_to_id',
                  'due_date', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')