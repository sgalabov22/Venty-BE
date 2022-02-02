from django.db import models
from django.utils import timezone

# Create your models here.
from users.models import Account


class LocationPosition(models.Model):
    lat = models.FloatField(max_length=15, blank=True, default=None)
    lng = models.FloatField(max_length=15, blank=True, default=None)

    def __str__(self):
        return f"{self.lat} --{self.lng}"


class WorkingHours(models.Model):
    weekly_text = models.CharField(max_length=1000, blank=True, default=None)


class Photos(models.Model):
    height = models.IntegerField(blank=True, default=None)
    width = models.IntegerField(blank=True, default=None)
    html_attributes= models.CharField(max_length=200, blank=True, default=None)


class LocationReview(models.Model):
    author_name = models.CharField(max_length=50, blank=True, default=None)
    author_url = models.URLField(blank=True, default=None)
    profile_photo_url = models.URLField(blank=True, default=None)
    rating = models.IntegerField(blank=True, default=None)
    relative_time_description = models.CharField(max_length=20, blank=True, default=None)
    text = models.CharField(max_length=300, blank=True, default=None)


class Location(models.Model):
    formatted_address = models.CharField(max_length=150, blank=True, default=None)
    international_phone_number = models.CharField(max_length=50, blank=True, default=None)
    name = models.CharField(max_length=100, blank=True, default=None)
    place_id = models.CharField(max_length=100, blank=True, default=None)
    rating = models.FloatField(max_length=15, blank=True, default=None)
    user_rating_total = models.IntegerField(blank=True, default=None)
    website = models.CharField(max_length=100, blank=True, default=None)

    geometry = models.OneToOneField(LocationPosition, on_delete=models.CASCADE)
    opening_hours = models.OneToOneField(WorkingHours, on_delete=models.CASCADE, null=True, default=None)
    photos = models.ManyToManyField(Photos, null=True, default=None)
    reviews = models.ManyToManyField(LocationReview, null=True, default=None)

    def __str__(self):
        return f"{self.name}"


class Event(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    start_date = models.DateTimeField(null=True, blank=True, default=None)
    end_date = models.DateTimeField(null=True, blank=True, default=None)
    event_title = models.CharField(max_length=30, default=None,
                                   help_text="Let your guest know details about this event")
    description = models.TextField(max_length=1000, blank=True)
    event_owner = models.ForeignKey(Account, on_delete=models.CASCADE)
    location = models.OneToOneField(Location, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.event_title}"
