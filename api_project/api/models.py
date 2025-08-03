from rest_framework.generics import ListAPIView
from django.db import models
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    permission_classes = [IsAuthenticated]  # Only logged-in users can view books

    def __str__(self):
        return self.title
