from .views import EventCategoriesListCreateView, EventCategoryDetailView
from django.urls import path



urlpatterns = [
    path('<int:event_id>/categories/', EventCategoriesListCreateView.as_view(), name='event-categories-list-create'),
    path('<int:event_id>/categories/<int:pk>/', EventCategoryDetailView.as_view(), name='event-category-detail'),
]