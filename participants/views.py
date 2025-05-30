from django.shortcuts import render
from rest_framework import generics
from .serializers import ParticipantSerializer
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from .models import *
# Create your views here.



class EventParticipantsListCreateView(generics.ListCreateAPIView):
    serializer_class = ParticipantSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        event_id = self.kwargs['event_id']
        return Participant.objects.filter(event_id=event_id)

    def perform_create(self, serializer):
        event = Event.objects.get(id=self.kwargs['event_id'])
        if not (self.request.user.is_superuser or self.request.user.coordinator == event.coordinator):
            raise PermissionError("You do not have permission to add participants to this event.")
        serializer.save(event=event)

class EventParticipantDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ParticipantSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        event_id = self.kwargs['event_id']
        return Participant.objects.filter(event_id=event_id)

    def get_object(self):
        obj = super().get_object()
        event = obj.event
        if not (self.request.user.is_superuser or self.request.user.coordinator == event.coordinator):
            raise PermissionError("You do not have permission to modify this participant.")
        return obj