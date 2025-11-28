from rest_framework import serializers

class TaskSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    title = serializers.CharField()
    due_date = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    estimated_hours = serializers.FloatField(required=False)
    importance = serializers.FloatField(required=False)
    dependencies = serializers.ListField(
        child=serializers.IntegerField(),
        required=False
    )
