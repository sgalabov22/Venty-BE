from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from events.models import Event, Location
from guests.models import Guest
from events.serializers import EventSerializerList, EventSerializerCreate, LocationSerializer, EventSerializerDetails
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class EventsList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            user_events_mapping = Guest.objects.filter(guest_user_account_id=request.user.id)
            events = Event.objects.filter(id__in=[r.event_id for r in user_events_mapping])
            serializer_data = EventSerializerList(events, many=True)
            return Response(serializer_data.data, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Not found"}, status=status.HTTP_400_BAD_REQUEST)


class EventCreate(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = request.data
        data["location"]["opening_hours"]["weekly_text"] = ", ".join(
            data["location"]["opening_hours"]["weekly_text"])

        serializer_data = EventSerializerCreate(data=data)
        serializer_data.is_valid(raise_exception=True)
        serializer_data.save(event_owner=self.request.user)
        last_event = Event.objects.last()
        last_event_serializer = EventSerializerDetails(last_event)
        data = last_event_serializer.data
        data["location"]["opening_hours"]["weekly_text"] = (
            data["location"]["opening_hours"]["weekly_text"].split(", "))
        return Response(data, status=status.HTTP_201_CREATED)


class EventDetailsGetUpdateDelete(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        try:
            event = Event.objects.get(id=pk)
            serializer_data = EventSerializerDetails(event)
            data = serializer_data.data
            data["location"]["opening_hours"]["weekly_text"] = (
                data["location"]["opening_hours"]["weekly_text"].split(", "))
            return Response(data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"message": "Not found"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            event = Event.objects.get(id=pk, event_owner=request.user)
            data = request.data
            data["location"]["opening_hours"]["weekly_text"] = ", ".join(
                data["location"]["opening_hours"]["weekly_text"])
            serializer_data = EventSerializerCreate(event, data=data)
            serializer_data.is_valid(raise_exception=True)
            serializer_data.save()
            updated_event = Event.objects.get(id=serializer_data.data["id"])
            serializer_updated_event = EventSerializerDetails(updated_event)
            data = serializer_updated_event.data
            data["location"]["opening_hours"]["weekly_text"] = (
                data["location"]["opening_hours"]["weekly_text"].split(", "))
            return Response(data)
        except:
            return Response({"message": "Not found"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            event = Event.objects.get(id=pk, event_owner=request.user)
            print(pk)
            print(request.user)
            print(event)

            event.delete()
            return Response({"message": "The Event has been deleted"}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Not found"}, status=status.HTTP_400_BAD_REQUEST)
