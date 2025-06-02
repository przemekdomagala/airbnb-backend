from django.db import models

class Property(models.Model):
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    max_guests = models.IntegerField()
    available_from = models.DateField()
    available_to = models.DateField()
    rating = models.FloatField(default=0.0)
    amenities = models.JSONField(default=list)  # lista udogodnień ["wifi", "parking", "klimatyzacja"]
    distance_to_center = models.FloatField(default=0.0)  # w km
    property_type = models.CharField(max_length=100, default="apartment")
    review_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title
