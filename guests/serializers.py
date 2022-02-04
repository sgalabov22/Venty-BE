from rest_framework import serializers

from guests.models import Guest
from users.models import Account


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
