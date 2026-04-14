from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=255)
    start = models.DateTimeField()
    end = models.DateTimeField(null=True, blank=True)

    color = models.CharField(max_length=20, default="#F472B6")

    def __str__(self):
        return self.title