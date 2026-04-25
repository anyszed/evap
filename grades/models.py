from django.db import models

class GradeTable(models.Model):
    name = models.CharField(max_length=100, default="Résultat")

    def __str__(self):
        return self.name


class Subject(models.Model):
    table = models.ForeignKey(GradeTable, on_delete=models.CASCADE, related_name='subjects')
    name = models.CharField(max_length=100)
    coefficient = models.FloatField(default=1)

    def __str__(self):
        return self.name


class Grade(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='grades')
    name = models.CharField(max_length=100, blank=True)
    value = models.FloatField()
    coefficient = models.FloatField(default=1)

    def __str__(self):
        return f"{self.value}"