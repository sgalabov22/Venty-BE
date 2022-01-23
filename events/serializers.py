from rest_framework import serializers
from events.models import Event, Guest
from users.models import Account


class EventSerializerList(serializers.ModelSerializer):
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
        exclude = ["id", "created_at", "event_owner"]


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["id", "fullname", "email", "profile_picture"]


class GuestSerializerList(serializers.ModelSerializer):
    guest_user_account = AccountSerializer()

    class Meta:
        model = Guest
        fields = ["guest_user_account", "status", "event"]


class GuestSerializerAdd(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = ["guest_user_account"]


class GuestSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = ["status"]
