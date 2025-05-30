from rest_framework import serializers
from coordinators.models import Coordinator
from users.serializers import UserSerializer

class CoordinatorSerializer(UserSerializer):
    class Meta:
        model = Coordinator
        fields = ['id', 'email', 'name', 'role', 'department']
        read_only_fields = ['id', 'role']

class CoordinatorRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = Coordinator
        fields = ['email', 'name', 'role', 'department', 'password']
        extra_kwargs = {
            'role': {'default': 'coordinator'},
        }

    def create(self, validated_data):
        user = Coordinator.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password'],
            department=validated_data.get('department', 'Event Management'),
            role='coordinator'  # Explicitly set role
        )
        return user