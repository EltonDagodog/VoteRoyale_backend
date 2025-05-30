from rest_framework import serializers
from users.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'role', 'is_active', 'is_staff', 'is_superuser']
        read_only_fields = ['id', 'is_staff', 'is_superuser']