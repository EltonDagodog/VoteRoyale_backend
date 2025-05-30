from .views import EventParticipantsListCreateView, EventParticipantDetailView
from django.urls import path



urlpatterns = [
    path('<int:event_id>/participants/', EventParticipantsListCreateView.as_view(), name='event-participants'),
    path('<int:event_id>/participants/<int:pk>/', EventParticipantDetailView.as_view(), name='event-participant-detail'),
   
]