from django.urls import path
from criteria.views import CriterionListCreateView, CriterionDetailView

urlpatterns = [
    # Event endpoints
    path('categories/<int:category_id>/criteria/', CriterionListCreateView.as_view(), name='criterion-list-by-category'),
    path('criteria/', CriterionListCreateView.as_view(), name='criterion-list-create'),
    path('categories/<int:category_id>/criteria/<int:id>/', CriterionDetailView.as_view(), name='criterion-detail'),
]