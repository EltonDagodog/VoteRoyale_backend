from .views import EventVotesListView,SubmitVoteView, JudgeDashboardView, CoordinatorEventVotesListView
from django.urls import path



urlpatterns = [
    path('<int:event_id>/votes/', EventVotesListView.as_view(), name='event-votes'),
    path('<int:event_id>/categories/<int:category_id>/vote/', SubmitVoteView.as_view(), name='submit_vote'),
    path('judges/dashboard/', JudgeDashboardView.as_view(), name='judge-dashboard'),
    path('coordinator/<int:event_id>/votes/', CoordinatorEventVotesListView.as_view(), name='coordinator-event-votes-list'),
]