from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    actor = serializers.StringRelatedField()  # display actor’s email
    target = serializers.StringRelatedField()

    class Meta:
        model = Notification
        fields = ["id", "actor", "verb", "target", "created_at", "is_read"]
