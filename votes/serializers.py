from rest_framework import serializers
from votes.models import Vote
from judges.serializers import JudgeSerializer
from participants.serializers import ParticipantSerializer
from categories.serializers import CategorySerializer
from events.serializers import EventSerializer

class VoteSerializer(serializers.ModelSerializer):
    judge = JudgeSerializer(read_only=True)
    participant = ParticipantSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    event = EventSerializer(read_only=True)
    criteria_scores = serializers.DictField(required=False, write_only=True)  # Add criteria_scores as write-only

    class Meta:
        model = Vote
        fields = ['id', 'judge', 'participant', 'category', 'event', 'score', 'comments', 'submitted_at', 'criteria_scores']
        read_only_fields = ['id', 'judge', 'participant', 'category', 'event', 'submitted_at']