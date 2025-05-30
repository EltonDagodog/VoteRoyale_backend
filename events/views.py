from rest_framework import generics # type: ignore
from rest_framework.permissions import IsAuthenticated # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore
from events.models import Event
from events.serializers import EventSerializer
from users.models import User
from django.shortcuts import get_object_or_404 # type: ignore


class EventDetailView(generics.RetrieveUpdateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        user = self.request.user
        if user.role != 'coordinator' and user.role != 'judge' and not user.is_superuser:
            raise PermissionError("Only coordinators and judge can view events")
        return obj

class EventListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EventSerializer
    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return Event.objects.all()

        if user.role == 'coordinator':
            return Event.objects.filter(coordinator=user.coordinator)

        return Event.objects.none()
    def perform_create(self, serializer):
        user = self.request.user
        if user.role != 'coordinator' and not user.is_superuser:
            raise PermissionError("Only coordinators can create events")
        serializer.save(coordinator=user.coordinator)

class EventUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EventSerializer
    queryset = Event.objects.all()

    def get_object(self):
        obj = super().get_object()
        user = self.request.user
        if user.role != 'coordinator' and not user.is_superuser:
            raise PermissionError("Only coordinators can update events")
        if obj.coordinator != user.coordinator and not user.is_superuser:
            raise PermissionError("You can only update your own events")
        return obj

class EventDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EventSerializer
    queryset = Event.objects.all()

    def get_object(self):
        obj = super().get_object()
        user = self.request.user
        if user.role != 'coordinator' and not user.is_superuser:
            raise PermissionError("Only coordinators can delete events")
        if obj.coordinator != user.coordinator and not user.is_superuser:
            raise PermissionError("You can only delete your own events")
        return obj