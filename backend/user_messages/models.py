from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class UserMessage(models.Model):
    title = models.CharField(max_length=256)
    body = models.TextField()
    sender = models.ForeignKey(
        User,
        related_name='sent_messages',
        on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        User,
        related_name='received_messages',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='When the message was first read by receiver.'
    )

    def __str__(self):
        return f'"{self.title}" from {self.sender} to {self.receiver}'
