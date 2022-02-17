from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from events.models import Event
from extensions.models import Checklist, Reminder
from extensions.serializers import ChecklistSerializer, ChecklistSerializerCreate, ReminderSerializer, \
    ChecklistSerializerDetails, ReminderSerializerDetails, ReminderSerializerCreate
from guests.models import Guest
from guests.serializers import AccountSerializer
from users.models import Account
from utility_functions.common import current_checklist_viewers, current_reminder_viewers, guests, event_guests


class ExtensionsGetCreate(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        event_list_guests = [guest_event.guest_user_account_id for guest_event in Guest.objects.filter(event=pk)]
        if request.user.id in event_list_guests:
            data = {}
            checklists_ext = Checklist.objects.filter(event=pk, viewers=request.user)
            reminders_ext = Reminder.objects.filter(event=pk, viewers=request.user)
            serializer_checklist_data = ChecklistSerializer(checklists_ext, many=True)
            serializer_reminder_data = ReminderSerializer(reminders_ext, many=True)
            data["checklist"] = [record for record in serializer_checklist_data.data]
            data["reminder"] = [record for record in serializer_reminder_data.data]
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Not found"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, pk):
        try:
            if request.query_params['type'] == "checklist" and request.user.id in event_guests(pk):
                serializer_data = ChecklistSerializerCreate(data=request.data)
                serializer_data.is_valid(raise_exception=True)
                event = Event.objects.get(id=pk)
                serializer_data.save(event=event)
                checklist_extension_last = Checklist.objects.last()
                checklist_extension_last.viewers.add(request.user)
                return Response(serializer_data.data, status=status.HTTP_201_CREATED)
            elif request.query_params['type'] == "reminder" and request.user.id in event_guests(pk):
                serializer_data = ReminderSerializerCreate(data=request.data)
                serializer_data.is_valid(raise_exception=True)
                event = Event.objects.get(id=pk)
                serializer_data.save(event=event)
                reminder_extension_last = Reminder.objects.last()
                reminder_extension_last.viewers.add(request.user)
                return Response(serializer_data.data, status=status.HTTP_201_CREATED)
        except ObjectDoesNotExist:
            return Response({"message": "Not found"}, status=status.HTTP_400_BAD_REQUEST)


class ExtensionsDetailsUpdate(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk, ext_id):
        data = {}
        if request.query_params['type'] == "checklist":
            checklists_ext = Checklist.objects.filter(event=pk, id=ext_id, viewers=request.user.id)
            serializer_checklist_data = ChecklistSerializerDetails(checklists_ext, many=True)
            data["checklist"] = [record for record in serializer_checklist_data.data]
        elif request.query_params['type'] == "reminder":
            reminders_ext = Reminder.objects.filter(event=pk, id=ext_id, viewers=request.user.id)
            serializer_reminder_data = ReminderSerializerDetails(reminders_ext, many=True)
            data["reminder"] = [record for record in serializer_reminder_data.data]
        if list(data.items())[0][1]:
            return Response(data, status=status.HTTP_200_OK)
        return Response({"message": "Not found"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, ext_id):
        if request.query_params['type'] == "checklist" and request.user in current_checklist_viewers(pk, ext_id):
            checklists_ext = Checklist.objects.filter(event=pk, id=ext_id, viewers=request.user.id)[0]
            serializer_data = ChecklistSerializer(checklists_ext, request.data)
            serializer_data.is_valid(raise_exception=True)
            event = Event.objects.get(id=pk)
            serializer_data.save(event=event)
            return Response(serializer_data.data, status=status.HTTP_200_OK)
        elif request.query_params['type'] == "reminder" and request.user in current_reminder_viewers(pk, ext_id):
            reminder_ext = Reminder.objects.filter(event=pk, id=ext_id, viewers=request.user.id)[0]
            serializer_data = ReminderSerializer(reminder_ext, request.data)
            serializer_data.is_valid(raise_exception=True)
            event = Event.objects.get(id=pk)
            serializer_data.save(event=event)
            return Response(serializer_data.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, ext_id):
        if request.query_params['type'] == "checklist":
            checklists_ext = Checklist.objects.filter(event=pk, id=ext_id, viewers=request.user.id)
            if checklists_ext:
                checklists_ext.delete()
                return Response({"message": "The Extension has been deleted"}, status=status.HTTP_200_OK)
        elif request.query_params['type'] == "reminder":
            reminder_ext = Reminder.objects.filter(event=pk, id=ext_id, viewers=request.user.id)
            if reminder_ext:
                reminder_ext[0].delete()
                return Response({"message": "The Extension has been deleted"}, status=status.HTTP_200_OK)
        return Response({"message": "Not found"}, status=status.HTTP_400_BAD_REQUEST)


class ExtensionsCatalogViewers(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk, ext_id):
        if request.query_params['type'] == "checklist" and request.user in current_checklist_viewers(pk, ext_id):
            available_viewers = [viewer for viewer in guests(pk) if viewer not in current_checklist_viewers(pk, ext_id)]
            serializer_user_catalog = AccountSerializer(available_viewers, many=True)
            return Response(serializer_user_catalog.data, status=status.HTTP_200_OK)
        elif request.query_params['type'] == "reminder" and request.user in current_reminder_viewers(pk, ext_id):
            available_viewers = [viewer for viewer in guests(pk) if viewer not in current_reminder_viewers(pk, ext_id)]
            serializer_user_catalog = AccountSerializer(available_viewers, many=True)
            return Response(serializer_user_catalog.data, status=status.HTTP_200_OK)
        return Response({"message": "Not found"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, pk, ext_id):
        if request.query_params['type'] == "checklist" and request.user in current_checklist_viewers(pk, ext_id):
            request_emails = [record['email'] for record in request.data]
            current_event_guests = Guest.objects.filter(event=pk)
            guest_emails = [record.guest_user_account.email for record in current_event_guests]
            checklist = Checklist.objects.get(event=pk, id=ext_id)
            current_checklist_emails = [record.email for record in checklist.viewers.all()]

            for email in request_emails:
                if email in guest_emails and email not in current_checklist_emails:
                    user = Account.objects.get(email=email)
                    checklist.viewers.add(user)

            serializer_data = ChecklistSerializer(checklist)
            return Response(serializer_data.data, status=status.HTTP_200_OK)
        elif request.query_params['type'] == "reminder" and request.user in current_reminder_viewers(pk, ext_id):
            request_emails = [record['email'] for record in request.data]
            current_event_guests = Guest.objects.filter(event=pk)
            guest_emails = [record.guest_user_account.email for record in current_event_guests]
            reminder = Reminder.objects.get(event=pk, id=ext_id)
            current_reminder_emails = [record.email for record in reminder.viewers.all()]

            for email in request_emails:
                if email in guest_emails and email not in current_reminder_emails:
                    user = Account.objects.get(email=email)
                    reminder.viewers.add(user)

            serializer_data = ReminderSerializer(reminder)
            return Response(serializer_data.data, status=status.HTTP_200_OK)
        return Response({"message": "Not found"}, status=status.HTTP_400_BAD_REQUEST)
