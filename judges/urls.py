from django.urls import path
from .views import EventJudgesListCreateView, EventJudgeDetailView, JudgeLoginView, JudgeDashboardView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('<int:event_id>/judges/', EventJudgesListCreateView.as_view(), name='event-judges'),
    path('<int:event_id>/judges/<int:pk>/', EventJudgeDetailView.as_view(), name='event-judge-detail'),
    path('judges/login/', JudgeLoginView.as_view(), name='judge-login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('judges/dashboard/', JudgeDashboardView.as_view(), name='judge-dashboard'),
]