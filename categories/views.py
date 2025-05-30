from rest_framework import generics # type: ignore
from rest_framework.permissions import IsAuthenticated # type: ignore
from rest_framework.exceptions import PermissionDenied # type: ignore
from categories.models import Category
from events.models import Event
from categories.serializers import CategorySerializer
from django.shortcuts import get_object_or_404

class EventCategoriesListCreateView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        event_id = self.kwargs['event_id']
        return Category.objects.filter(event_id=event_id)  # Already fixed typo

    def perform_create(self, serializer):
        event = get_object_or_404(Event, id=self.kwargs['event_id'])
        print(f"User: {self.request.user}, Role: {getattr(self.request.user, 'role', '')}, Superuser: {self.request.user.is_superuser}, Event Coordinator ID: {event.coordinator.id}, User ID: {self.request.user.id}")
        # Allow superusers or the event's coordinator to create categories
        if not (self.request.user.is_superuser or 
                (getattr(self.request.user, 'role', '') == "coordinator" and self.request.user.id == event.coordinator.id)):
            raise PermissionDenied("You do not have permission to add categories to this event.")
        serializer.save(event=event)
        
class EventCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        event_id = self.kwargs['event_id']
        return Category.objects.filter(event_id=event_id)

    def get_object(self):
        obj = super().get_object()
        event = obj.event
        user = self.request.user

        # Allow retrieval for judges, coordinators, and superusers
        can_retrieve = (
            user.is_superuser or
            user.role == "judge" or
            user.role == "coordinator"
        )

        # For update/destroy, only allow superusers or the event's coordinator
        can_modify = (
            user.is_superuser or
            user.role == "coordinator"
        )

        # Check the request method to apply appropriate permissions
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            if not can_modify:
                raise PermissionDenied("You do not have permission to modify this category.")
        else:  # GET request (retrieve)
            if not can_retrieve:
                raise PermissionDenied("You do not have permission to view this category.")

        return obj