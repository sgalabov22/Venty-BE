from rest_framework import viewsets
from events.models import Event
from events.serializers import EventSerializer



class EventViewSet(viewsets.ViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
