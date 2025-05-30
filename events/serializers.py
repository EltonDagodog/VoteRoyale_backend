from rest_framework import serializers
from events.models import Event
from coordinators.serializers import CoordinatorSerializer

class EventSerializer(serializers.ModelSerializer):
    coordinator = CoordinatorSerializer(read_only=True)

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'date', 'status', 'location', 'max_participants', 'coordinator']
        read_only_fields = ['id']