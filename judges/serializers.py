from rest_framework import serializers
from judges.models import Judge
from users.serializers import UserSerializer
from events.serializers import EventSerializer
import re

class JudgeSerializer(UserSerializer):
    event = EventSerializer(read_only=True)

    class Meta:
        model = Judge
        fields = ['id', 'email', 'name', 'role', 'access_code', 'event', 'specialization', 'image']
        read_only_fields = ['id', 'role', 'access_code', 'event']
        extra_kwargs = {
            'password': {'required': False, 'write_only': True},
            'username': {'required': False},
        }

    
    def create(self, validated_data):
        validated_data.pop('password', None)
        validated_data.pop('username', None)
        validated_data['role'] = 'judge'

        # Use the event and access_code passed via serializer.save()
        event = self.context['view'].kwargs.get('event_id')
        access_code = validated_data.pop('access_code', None)

        judge = Judge.objects.create(
            email=validated_data['email'],
            name=validated_data.get('name', ''),
            role='judge',
            specialization=validated_data['specialization'],
            image=validated_data.get('image', ''),
            access_code=access_code,
            event_id=event,  # Set the event_id directly
        )
        return judge

    def update(self, instance, validated_data):
        validated_data.pop('password', None)
        validated_data.pop('username', None)
        instance.email = validated_data.get('email', instance.email)
        instance.name = validated_data.get('name', instance.name)
        instance.specialization = validated_data.get('specialization', instance.specialization)
        instance.image = validated_data.get('image', instance.image)
        if 'access_code' in validated_data:
            instance.access_code = validated_data['access_code']
        instance.save()
        return instance