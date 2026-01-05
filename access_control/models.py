from django.db import models

# Create your models here.

class AccessLog(models.Model):
    card_id = models.CharField(max_length=50)
    door_name = models.CharField(max_length=100)
    access_granted = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        status = "GRANTED" if self.access_granted else "DENIED"
        return f"{self.timestamp}: Access {status} for card {self.card_id} at door {self.door_name}"

