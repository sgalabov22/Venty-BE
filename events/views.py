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

from utility.working_hours import working_hours_as_list, working_hours_as_string

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
        data_wh_string = working_hours_as_string(request.data)
        serializer_data = EventSerializerCreate(data=data_wh_string)
        serializer_data.is_valid(raise_exception=True)
        serializer_data.save(event_owner=self.request.user)
        last_event = Event.objects.last()
        last_event_serializer = EventSerializerDetails(last_event)
        serializer_data_copy = last_event_serializer.data
        data = working_hours_as_list(serializer_data_copy)
        return Response(data, status=status.HTTP_201_CREATED)


class EventDetailsGetUpdateDelete(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        try:
            event = Event.objects.get(id=pk)
            serializer_data = EventSerializerDetails(event)
            serializer_data_copy = serializer_data.data
            data = working_hours_as_list(serializer_data_copy)
            return Response(data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"message": "Not found"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            data_wh_string = working_hours_as_string(request.data)
            event = Event.objects.get(id=pk, event_owner=request.user)
            serializer_data = EventSerializerCreate(event, data=data_wh_string)
            serializer_data.is_valid(raise_exception=True)
            serializer_data.save()
            updated_event = Event.objects.get(id=serializer_data.data["id"])
            serializer_updated_event = EventSerializerDetails(updated_event)
            serializer_data_copy = serializer_updated_event.data
            data = working_hours_as_list(serializer_data_copy)
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
