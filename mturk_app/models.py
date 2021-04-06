from django.db import models

# Create your models here.

class Participant(models.Model):
    data = models.JSONField(max_length=None)
    load_date = models.DateTimeField(auto_now_add=True, null=True)
    worker_id = models.CharField(max_length=100)
    assignment_id = models.CharField(max_length=100)
    hit_id = models.CharField(max_length=100)

    def __str__(self):
        return f" {self.worker_id} {self.load_date}"