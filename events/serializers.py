from rest_framework import serializers
from events.models import Event
from django.utils import timezone


#ToDo nested Sirializers


# class GuestSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Guest
#         fields = ['order', 'title', 'duration']
#
# class ExampleSerializer(serializers.ModelSerializer):
#     tracks = TrackSerializer(many=True)




class EventSerializerFullInfo(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class EventSerializerCreate(serializers.ModelSerializer):
    def validate(self, data):
        if not data["event_title"][0].isupper():
            raise serializers.ValidationError("Title must start with capital")
        return data
        # if data["start_date"] > ["end_date"]:
        #     raise serializers.ValidationError("Start date must be before End date of the event")
        # return data

    class Meta:
        model = Event
        exclude = ["id", "created_at", "modified_at", "event_owner"]


class EventSerializerUpdate(serializers.ModelSerializer):
    def validate(self, data):
        if not data["event_title"][0].isupper():
            raise serializers.ValidationError("Title must start with capital")
#todo to fix the validations
        # if data["start_date"] > ["end_date"]:
        #     raise serializers.ValidationError("Start date must be before End date of the event")

        # if data["modified_at"] < timezone.now:
        #     data["modified_at"] = timezone.now
        return data

    class Meta:
        model = Event
        exclude = ["id", "created_at", "event_owner"]
