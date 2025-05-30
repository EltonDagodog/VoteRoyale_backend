from rest_framework import serializers
from participants.models import Participant
from events.serializers import EventSerializer
from categories.serializers import CategorySerializer

class ParticipantSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)

    class Meta:
        model = Participant
        fields = ['id', 'name', 'event', 'entry', 'registration_date', 'contestant_number', 'email', 'origin', 'gender', 'image']
        read_only_fields = ['id']