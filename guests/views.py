from rest_framework.response import Response
from rest_framework.views import APIView
from events.models import Event
from guests.models import Guest
from guests.serializers import GuestSerializerList, GuestSerializerAdd, GuestSerializerUpdate, AccountSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth import get_user_model
from users.models import Account
from django.core.exceptions import ObjectDoesNotExist

from utility_functions.common import event_guests

UserModel = get_user_model()


# Create your views here.
class EventGuestGetCreate(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        try:
            if request.user in event_guests(pk):
                try:
                    guest_event = Guest.objects.filter(event=pk)
                    serializer_guest_data = GuestSerializerList(guest_event, many=True)
                    return Response(serializer_guest_data.data, status=status.HTTP_200_OK)
                except ObjectDoesNotExist:
                    return Response({"message": "Not found"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "Not found"}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
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
        except ObjectDoesNotExist:
            return Response({"message": "Not found"}, status=status.HTTP_400_BAD_REQUEST)


class EventGuestUpdate(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, pk, guest_pk):
        try:
            guest = Guest.objects.get(event=pk, id=guest_pk)
            serializer_guest_data = GuestSerializerUpdate(guest, data=request.data)
            serializer_guest_data.is_valid(raise_exception=True)
            serializer_guest_data.save()
            return Response(serializer_guest_data.validated_data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
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
        except ObjectDoesNotExist:
            return Response({"message": "Not found"}, status=status.HTTP_400_BAD_REQUEST)
