from rest_framework import serializers
from criteria.models import Criterion
from rest_framework import serializers

class CriterionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Criterion
        fields = ['id', 'name', 'description', 'percentage']

    def validate_percentage(self, value):
        if value <= 0 or value > 100:
            raise serializers.ValidationError("Percentage must be between 0 and 100.")
        return value