from rest_framework import serializers

class TodoItemSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(required=False)
    bucket_uuid = serializers.UUIDField(required=False)
    title = serializers.CharField(max_length=255, required=True)
    body = serializers.CharField(required=True)
    is_completed = serializers.BooleanField(required=False)

class BucketSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(required=False)
    name = serializers.CharField(max_length=255, required=True)
    copy_from = serializers.UUIDField(required=False)
