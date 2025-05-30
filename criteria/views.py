from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from criteria.models import Criterion
from criteria.serializers import CriterionSerializer
from categories.models import Category

class CriterionListCreateView(generics.ListCreateAPIView):
    serializer_class = CriterionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        if category_id:
            return Criterion.objects.filter(category_id=category_id)
        return Criterion.objects.all()

    def perform_create(self, serializer):
        category_id = self.request.data.get('category_id')
        category = Category.objects.get(id=category_id)
        event = category.event
        if not (self.request.user.is_superuser or self.request.user == event.coordinator):
            raise PermissionDenied("You do not have permission to add criteria to this category.")
        serializer.save(category=category)

class CriterionDetailView(generics.DestroyAPIView):
    serializer_class = CriterionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        if category_id:
            return Criterion.objects.filter(category_id=category_id)
        return Criterion.objects.all()

    def get_object(self):
        obj = super().get_object()
        event = obj.category.event
        if not (self.request.user.is_superuser or self.request.user == event.coordinator):
            raise PermissionDenied("You do not have permission to delete this criterion.")
        return obj