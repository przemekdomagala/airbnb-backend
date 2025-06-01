from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"{self.name} ({self.location})"

class MapMarker(models.Model):
    MARKER_TYPES = [
        ('property', 'Property'),
        ('poi', 'Point of Interest'),
        ('custom', 'Custom'),
    ]
    location = models.ForeignKey('Location', on_delete=models.CASCADE, related_name='markers')
    marker_type = models.CharField(max_length=20, choices=MARKER_TYPES, default='custom')
    label = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.label} [{self.marker_type}]"

class POI(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.ForeignKey('Location', on_delete=models.CASCADE, related_name='pois')

    def __str__(self):
        return self.name

class MapAnnotation(models.Model):
    location = models.ForeignKey('Location', on_delete=models.CASCADE, related_name='annotations')
    text = models.TextField()

    def __str__(self):
        return f"Annotation on {self.location.name}"

class MapBookmark(models.Model):
    user_id = models.IntegerField()
    location = models.ForeignKey('Location', on_delete=models.CASCADE, related_name='bookmarks')

    def __str__(self):
        return f"Bookmark by user {self.user_id} for {self.location.name}"

class MapLegend(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title

class MapUpdate(models.Model):
    description = models.TextField()
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Update at {self.updated_at}"

class MapDownload(models.Model):
    user_id = models.IntegerField()
    downloaded_at = models.DateTimeField(auto_now_add=True)
    data_summary = models.TextField()

    def __str__(self):
        return f"Download by {self.user_id} at {self.downloaded_at}"

class UserInteraction(models.Model):
    INTERACTION_TYPES = [
        ('click', 'Click'),
        ('zoom', 'Zoom'),
        ('hover', 'Hover'),
        ('pan', 'Pan'),
        ('search', 'Search'),
    ]
    user_id = models.IntegerField()
    interaction_type = models.CharField(max_length=20, choices=INTERACTION_TYPES)
    interaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.interaction_type} by {self.user_id}"

class MapTooltip(models.Model):
    location = models.ForeignKey('Location', on_delete=models.CASCADE, related_name='tooltips')
    text = models.CharField(max_length=200)

    def __str__(self):
        return f"Tooltip for {self.location.name}"
