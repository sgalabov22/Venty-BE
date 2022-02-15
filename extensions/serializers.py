from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers
from extensions.models import Checklist, ChecklistItems, Reminder
from guests.serializers import AccountSerializer



class ItemsSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    class Meta:
        model = ChecklistItems
        fields = "__all__"


class ViewersSerializer(WritableNestedModelSerializer, AccountSerializer):
    pass


class ChecklistSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    items = ItemsSerializer(required=False, many=True)
    viewers = ViewersSerializer(required=False, many=True)

    class Meta:
        model = Checklist
        fields = ['id', 'name', 'event', 'items', 'viewers']


class ReminderSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    viewers = ViewersSerializer(required=False, many=True)

    class Meta:
        model = Reminder
        fields = ['id', 'name', 'scheduled', 'email_body', 'event', 'viewers']


class ChecklistSerializerCreate(ChecklistSerializer, WritableNestedModelSerializer):
    class Meta:
        model = Checklist
        exclude = ("id",)


class ReminderSerializerCreate(ReminderSerializer, WritableNestedModelSerializer):
    class Meta:
        model = Reminder
        exclude = ("id",)


class ChecklistSerializerDetails(ChecklistSerializerCreate):
    pass


class ReminderSerializerDetails(ReminderSerializerCreate):
    pass
