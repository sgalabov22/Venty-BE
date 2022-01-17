from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from events.models import Event
from events.serializers import EventSerializerFullInfo, EventSerializerCreate, EventSerializerUpdate
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from oauth2_provider.models import AccessToken
from rest_framework import status
from django.utils import timezone


# class EventViewSet(viewsets.ViewSet):
#     serializer_class = EventSerializer
#     queryset = Event.objects.all()

#TODo to create view about the guests

class EventsList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        token = request.headers.get('Authorization').split()[1]
        user_id = AccessToken.objects.get(token=token).user_id
        events = Event.objects.filter(event_owner_id=user_id)
        serializer_data = EventSerializerFullInfo(events, many=True)

        return Response(serializer_data.data, status=status.HTTP_201_CREATED)


class EventCreate(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer_data = EventSerializerCreate(data=request.data)
        if serializer_data.is_valid():
            serializer_data.save(event_owner=self.request.user)
            return Response(serializer_data.validated_data, status=status.HTTP_201_CREATED)
        return Response(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)


class EventGetUpdateDelete(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, pk):
        try:
            event = Event.objects.get(id=pk)
            serializer_data = EventSerializerUpdate(event, data=request.data)
            if serializer_data.is_valid():
                serializer_data.save()
                return Response(serializer_data.validated_data)
            return Response(serializer_data.errors)
        except:
            return Response({"message": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        print(pk)
        try:
            event = Event.objects.get(id=pk)
            serializer_data = EventSerializerFullInfo(event)
            return Response(serializer_data.data, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            event = Event.objects.get(id=pk)
            event.delete()
            return Response({"message": "The Event was deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as ex:
            return Response({"message": "Not found"}, status=status.HTTP_404_NOT_FOUND)
