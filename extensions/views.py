from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from events.models import Event
from extensions.models import Checklist, Reminder
from extensions.serializers import ChecklistSerializer, ChecklistSerializerCreate, ReminderSerializer, \
    ChecklistSerializerDetails, ReminderSerializerDetails, ReminderSerializerCreate
from guests.models import Guest


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
        event_list_guests = [guest_event.guest_user_account_id for guest_event in Guest.objects.filter(event=pk)]
        if request.user.id in event_list_guests and request.GET.get("type") == "checklist":

            serializer_data = ChecklistSerializerCreate(data=request.data)
            serializer_data.is_valid(raise_exception=True)
            event = Event.objects.get(id=pk)
            serializer_data.save(event=event)
            checklist_extension_last = Checklist.objects.last()
            checklist_extension_last.viewers.add(request.user)

        elif request.user.id in event_list_guests and request.GET.get("type") == "reminder":
            serializer_data = ReminderSerializerCreate(data=request.data)
            serializer_data.is_valid(raise_exception=True)
            event = Event.objects.get(id=pk)
            serializer_data.save(event=event)
            reminder_extension_last = Reminder.objects.last()
            reminder_extension_last.viewers.add(request.user)

        try:
            return Response(serializer_data.data, status=status.HTTP_201_CREATED)
        except:
            return Response({"message": "Not found"}, status=status.HTTP_400_BAD_REQUEST)


class ExtensionsDetailsUpdate(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk, ext_id):
        data = {}
        if request.GET.get("type") == "checklist":
            checklists_ext = Checklist.objects.filter(event=pk, id=ext_id, viewers=request.user.id)
            serializer_checklist_data = ChecklistSerializerDetails(checklists_ext, many=True)
            data["checklist"] = [record for record in serializer_checklist_data.data]
        elif request.GET.get("type") == "reminder":
            reminders_ext = Reminder.objects.filter(event=pk, id=ext_id, viewers=request.user.id)
            serializer_reminder_data = ReminderSerializerDetails(reminders_ext, many=True)
            data["reminder"] = [record for record in serializer_reminder_data.data]

        if list(data.items())[0][1]:
            return Response(data, status=status.HTTP_200_OK)
        return Response({"message": "Not found"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, ext_id):
        viewers_list_checklist = [viewers.id for checklist in Checklist.objects.filter(event=pk, id=ext_id) for viewers
                                  in checklist.viewers.all()]
        viewers_list_reminder = [viewers.id for checklist in Reminder.objects.filter(event=pk, id=ext_id) for viewers in
                                 checklist.viewers.all()]

        if request.GET.get("type") == "checklist" and request.user.id in viewers_list_checklist:
            checklists_ext = Checklist.objects.filter(event=pk, id=ext_id, viewers=request.user.id)[0]
            serializer_data = ChecklistSerializer(checklists_ext, request.data)
        elif request.GET.get("type") == "reminder" and request.user.id in viewers_list_reminder:
            reminder_ext = Reminder.objects.filter(event=pk, id=ext_id, viewers=request.user.id)[0]
            serializer_data = ReminderSerializer(reminder_ext, request.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            serializer_data.is_valid(raise_exception=True)
            event = Event.objects.get(id=pk)
            serializer_data.save(event=event)
            serializer_data.save()
            return Response(serializer_data.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, ext_id):

        if request.GET.get("type") == "checklist":
            checklists_ext = Checklist.objects.filter(event=pk, id=ext_id, viewers=request.user.id)
            if checklists_ext:
                checklists_ext.delete()
                return Response({"message": "The Extension has been deleted"}, status=status.HTTP_200_OK)
        elif request.GET.get("type") == "reminder":
            reminder_ext = Reminder.objects.filter(event=pk, id=ext_id, viewers=request.user.id)
            if reminder_ext:
                reminder_ext[0].delete()
                return Response({"message": "The Extension has been deleted"}, status=status.HTTP_200_OK)
        return Response({"message": "Not found"}, status=status.HTTP_400_BAD_REQUEST)
