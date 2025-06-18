from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Host(models.Model):
    user_id = models.IntegerField(default=0)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    rating = models.FloatField(default=0.0)
    image = models.URLField()
    details = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.location})"


class HostAvailability(models.Model):
    host = models.ForeignKey('Host', on_delete=models.CASCADE, related_name='availabilities')
    start_date = models.DateField()
    end_date = models.DateField()

    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError('Start date must be before end date.')

    def __str__(self):
        return f"{self.host.name}: {self.start_date} - {self.end_date}"
