from django.db import models

class Note(models.Model):
    title = models.CharField(max_length=255, blank=True)
    content = models.TextField(blank=True)

    is_deleted = models.BooleanField(default=False)
    position = models.IntegerField(default=0)
    is_pinned = models.BooleanField(default=False)

    color = models.CharField(max_length=50, default="bg-pink-100")