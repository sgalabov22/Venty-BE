from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework.views import APIView
from events.models import Event
from guests.models import Guest
from events.serializers import EventSerializer, EventSerializerCreate
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
            serializer_data = EventSerializer(events, many=True)
            return Response(serializer_data.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"message": "Not found"}, status=status.HTTP_400_BAD_REQUEST)


class EventCreate(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer_data = EventSerializerCreate(data=request.data)
        serializer_data.is_valid(raise_exception=True)
        serializer_data.save(event_owner=request.user)
        last_event = Event.objects.last()
        last_event_serializer = EventSerializer(last_event)

        return Response(last_event_serializer.data, status=status.HTTP_201_CREATED)


class EventDetailsGetUpdateDelete(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        try:
            user_events_mapping = Guest.objects.filter(guest_user_account_id=request.user.id)
            event = Event.objects.filter(id__in=[r.event_id for r in user_events_mapping]).get(id=pk)
            serializer_data = EventSerializer(event)
            return Response(serializer_data.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"message": "Not found"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            event = Event.objects.get(id=pk, event_owner=request.user)
            serializer_data = EventSerializerCreate(event, data=request.data)
            if serializer_data.is_valid():
                serializer_data.save()
                return Response(serializer_data.validated_data, status=status.HTTP_200_OK)
            return Response(serializer_data.errors)
        except ObjectDoesNotExist:
            return Response({"message": "Not found"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            event = Event.objects.get(id=pk, event_owner=request.user)
            event.delete()
            return Response({"message": "The Event has been deleted"}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"message": "Not found"}, status=status.HTTP_400_BAD_REQUEST)
