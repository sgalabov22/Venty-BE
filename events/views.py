from rest_framework.response import Response
from rest_framework.views import APIView
from events.models import Event, Guest
from events.serializers import EventSerializerList, EventSerializerCreate, GuestSerializerList, GuestSerializerAdd, \
    GuestSerializerUpdate, AccountSerializer

from rest_framework.permissions import IsAuthenticated
from oauth2_provider.models import AccessToken
from rest_framework import status
from django.contrib.auth import get_user_model
from users.models import Account

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
        serializer_data = EventSerializerCreate(data=request.data)
        serializer_data.is_valid(raise_exception=True)
        serializer_data.save(event_owner=self.request.user)
        last_event = Event.objects.last()
        last_event_serializer = EventSerializerList(last_event)
        return Response(last_event_serializer.data, status=status.HTTP_201_CREATED)


class EventDetailsGetUpdateDelete(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        try:
            event = Event.objects.get(id=pk)
            serializer_data = EventSerializerList(event)
            return Response(serializer_data.data, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Not found"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            event = Event.objects.get(id=pk, event_owner=request.user)
            serializer_data = EventSerializerCreate(event, data=request.data)
            serializer_data.is_valid(raise_exception=True)
            serializer_data.save()
            updated_event = Event.objects.get(id=serializer_data.data["id"])
            serializer_updated_event = EventSerializerList(updated_event)
            return Response(serializer_updated_event.data)
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


class EventGuestGetCreate(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        try:
            event = Event.objects.get(id=pk)
            if request.user.id == event.event_owner.id:
                try:
                    guest_event = Guest.objects.filter(event=pk)
                    serializer_guest_data = GuestSerializerList(guest_event, many=True)
                    return Response(serializer_guest_data.data, status=status.HTTP_200_OK)
                except:
                    return Response({"message": "Not found"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "Not found"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"message": "Not found"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, pk):
        try:
            event = Event.objects.get(pk=pk)
            if request.user.id == event.event_owner_id:
                guests = Guest.objects.filter(event_id=pk)
                list_guests = [guest.guest_user_account.id for guest in guests]
                data = [record for record in request.data if record["guest_user_account"] not in list_guests]
                if len(data) != 0:
                    serializer_data = GuestSerializerAdd(data=data, many=True)
                    serializer_data.is_valid(raise_exception=True)
                    serializer_data.save(event=event)
                    return Response(serializer_data.data, status=status.HTTP_201_CREATED)
                return Response(status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "Not found"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"message": "Not found"}, status=status.HTTP_400_BAD_REQUEST)

class EventGuestUpdate(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, pk, guest_pk):
        try:
            guest = Guest.objects.filter(guest_user_account=guest_pk)[0]
            serializer_guest_data = GuestSerializerUpdate(guest, data=request.data)
            if serializer_guest_data.is_valid():
                serializer_guest_data.save()
                return Response(serializer_guest_data.validated_data, status=status.HTTP_200_OK)
            return Response(serializer_guest_data.errors)
        except:
            return Response({"message": "Not found"}, status=status.HTTP_400_BAD_REQUEST)


class EventGuestCatalogUsers(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        try:
            event = Event.objects.get(pk=pk)

            if request.user.id == event.event_owner_id:
                guests = Guest.objects.filter(event_id=pk)
                accounts = Account.objects.all()

                list_guests = [guest.guest_user_account.id for guest in guests]
                available_guests = [record for record in accounts if record.id not in list_guests]

                serializer_user_catalog = AccountSerializer(available_guests, many=True)
                return Response(serializer_user_catalog.data, status=status.HTTP_200_OK)
            return Response({"message": "Not found"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"message": "Not found"}, status=status.HTTP_400_BAD_REQUEST)