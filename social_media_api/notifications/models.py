from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

User = get_user_model()

class Notification(models.Model):
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notifications"
    )
    actor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="actor_notifications"
    )
    verb = models.CharField(max_length=255)  # e.g. "liked your post", "followed you"
    
    # Generic relation to any object (Post, Comment, etc.)
    target_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    target_object_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey("target_content_type", "target_object_id")

    # ✅ timestamp field
    timestamp = models.DateTimeField(auto_now_add=True)

    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.actor} {self.verb} {self.target} -> {self.recipient}"
