from rest_framework import serializers
from .models import Category
from criteria.models import Criterion
from events.serializers import EventSerializer
from criteria.serializers import CriterionSerializer

class CategorySerializer(serializers.ModelSerializer):
    criteria = CriterionSerializer(many=True, required=False)

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'max_score', 'weight', 'status', 'gender', 'criteria', 'award_type']

    def validate(self, data):
        # Validate that criteria percentages sum to 100%
        criteria = data.get('criteria', [])
        total_percentage = sum(criterion['percentage'] for criterion in criteria)
        if criteria and total_percentage != 100:
            raise serializers.ValidationError("Criteria percentages must total exactly 100%.")
        return data

    def create(self, validated_data):
        criteria_data = validated_data.pop('criteria', [])
        category = Category.objects.create(**validated_data)
        for criterion_data in criteria_data:
            Criterion.objects.create(category=category, **criterion_data)
        return category

    def update(self, instance, validated_data):
        criteria_data = validated_data.pop('criteria', [])
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.max_score = validated_data.get('max_score', instance.max_score)
        instance.weight = validated_data.get('weight', instance.weight)
        instance.status = validated_data.get('status', instance.status)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.award_type = validated_data.get('award_type', instance.award_type)  # Update award_type
        instance.save()

        # Update criteria
        instance.criteria.all().delete()  # Remove existing criteria
        for criterion_data in criteria_data:
            Criterion.objects.create(category=instance, **criterion_data)
        return instance