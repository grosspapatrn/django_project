from django.utils import timezone
from rest_framework import serializers
from datetime import date
from TaskManager.models import (
    Task,
    SubTask,
    Category,
)

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'status',
            'deadline',
        ]


class SubTaskSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = SubTask
        fields = [
            'id',
            'title',
            'description',
            'task',
            'status',
            'deadline',
            'created_at',
        ]


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'name',
            'description',
            ]


    def create(self, validated_data):
        name = validated_data.get('name')
        if Category.objects.filter(name=name).exists():
            raise serializers.ValidationError({'name': 'Category already exists'})
        return super().create(validated_data)


    def update(self, instance, validated_data):
        name = validated_data.get('name', instance.name)
        if Category.objects.filter(name=name).exclude(pk=instance.pk).exists():
            raise serializers.ValidationError({'name': 'Category already exists'})
        return super().update(instance, validated_data)


class TaskDetailSerializer(serializers.ModelSerializer):
    subtask = SubTaskSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'status',
            'deadline',
        ]


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'title',
            'description',
            'deadline',
        ]

    def validate_deadline(self, value):
        if value < date.today():
            raise serializers.ValidationError({'deadline': 'Deadline date should be in the future'})
        return value