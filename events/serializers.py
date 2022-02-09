from rest_framework import serializers
from events.models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"


class EventSerializerCreate(serializers.ModelSerializer):
    def validate(self, data):
        if not data["event_title"][0].isupper():
            data["event_title"] = data["event_title"][0].upper() + data["event_title"][1:]
        if data["start_date"] > data["end_date"]:
            raise serializers.ValidationError("Start date must be before End date of the event")
        return data

    class Meta:
        model = Event
        exclude = ["event_owner"]