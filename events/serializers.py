from rest_framework import serializers
from events.models import Event, Location, LocationPosition, WorkingHours, Photos, LocationReview
from drf_writable_nested import WritableNestedModelSerializer

class EventSerializerList(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"


class LocationPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationPosition
        exclude = ["id"]


class OpeningHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkingHours
        exclude = ["id"]


class PhotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photos
        exclude = ["id"]


class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationReview
        exclude = ["id"]


class LocationSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    geometry = LocationPositionSerializer(required=False)
    opening_hours = OpeningHoursSerializer(required=False)
    photos = PhotosSerializer(required=False, many=True)
    reviews = ReviewsSerializer(required=False, many=True)

    class Meta:
        model = Location
        exclude = ["id"]


class EventSerializerDetails(serializers.ModelSerializer):
    location = LocationSerializer()

    class Meta:
        model = Event
        fields = ["id", "created_at", "start_date", "end_date", "event_title", "description", "event_owner",
                  "location"]


class EventSerializerCreate(WritableNestedModelSerializer,serializers.ModelSerializer):
    location = LocationSerializer()

    def validate(self, data):
        if not data["event_title"][0].isupper():
            data["event_title"] = data["event_title"][0].upper() + data["event_title"][1:]
        if data["start_date"] > data["end_date"]:
            raise serializers.ValidationError("Start date must be before End date of the event")
        return data

    class Meta:
        model = Event
        exclude = ["event_owner"]
