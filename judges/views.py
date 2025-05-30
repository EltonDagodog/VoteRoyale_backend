# judges/views.py
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail, get_connection
from django.conf import settings
from .models import Judge
from .serializers import JudgeSerializer
from participants.models import Participant
from participants.serializers import ParticipantSerializer
from categories.models import Category
from categories.serializers import CategorySerializer
from votes.models import Vote
from votes.serializers import VoteSerializer
from events.models import Event  # Assuming these models exist
from events.serializers import EventSerializer # Add these serializers
import random
import string

class JudgeLoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        access_code = request.data.get('access_code', '').upper()
        if not access_code:
            return Response(
                {"error": "Access code is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            judge = Judge.objects.get(access_code=access_code, role="judge")
            user = judge
        except Judge.DoesNotExist:
            return Response(
                {"error": "Invalid access code"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        return Response({
            "message": "Access granted",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "judge": {
                "role": "judge",
                "name": user.name,
                "email": user.email,
                "event": user.event.id,
                "access_code": user.access_code
            }
        }, status=status.HTTP_200_OK)

class JudgeDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get the Judge instance based on the authenticated user
        try:
            judge = Judge.objects.get(id=request.user.id)  # Match by ID
            if judge.role != "judge":
                return Response(
                    {"error": "User is not a judge"},
                    status=status.HTTP_403_FORBIDDEN
                )
        except Judge.DoesNotExist:
            return Response(
                {"error": "Judge profile not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        event = judge.event
        # Fetch participants, categories, and votes for the event
        participants = Participant.objects.filter(event=event)
        categories = Category.objects.filter(event=event)
        votes = Vote.objects.filter(judge=judge)

        return Response({
            "judge": {
                "name": judge.name,
                "email": judge.email,
                "access_code": judge.access_code,
                "event_id": event.id,
                "specialization": judge.specialization,
                "image": judge.image,
            },
            "event": {
                "id": event.id,
                "title": event.title,
                "description": event.description,
                "date": event.date,
                "status": event.status,
                "location": event.location,
                "max_participants": event.max_participants,
            },
            "participants": ParticipantSerializer(participants, many=True).data,
            "categories": CategorySerializer(categories, many=True).data,
            "votes": VoteSerializer(votes, many=True).data,
        }, status=status.HTTP_200_OK)

class EventJudgesListCreateView(generics.ListCreateAPIView):
    serializer_class = JudgeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        event_id = self.kwargs['event_id']
        return Judge.objects.filter(event_id=event_id)

    def perform_create(self, serializer):
        event = Event.objects.get(id=self.kwargs['event_id'])
        if not (self.request.user.is_superuser or self.request.user.coordinator == event.coordinator):
            raise PermissionError("You do not have permission to add judges to this event.")
        while True:
            access_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            if not Judge.objects.filter(access_code=access_code).exists():
                break
        judge = serializer.save(event=event, access_code=access_code, role="judge")
        print("Current EMAIL_BACKEND:", settings.EMAIL_BACKEND)
        subject = 'Your Judge Access Code'
        message = f'Hello {judge.name},\n\nYour access code for the event "{event.title}" is: {access_code}\n\nUse this code to log in to the voting system.\n\nBest,\nVoteRoyale Team'
        from_email = 'dagodogelton79email@gmail.com'
        recipient_list = [judge.email]
        try:
            connection = get_connection()
            print("Using connection:", connection)
            send_mail(subject, message, from_email, recipient_list, fail_silently=True)
        except Exception as e:
            print(f"Failed to send email to {judge.email}: {e}")

class EventJudgeDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = JudgeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        event_id = self.kwargs['event_id']
        return Judge.objects.filter(event_id=event_id)

    def get_object(self):
        obj = super().get_object()
        event = obj.event
        if not (self.request.user.is_superuser or self.request.user.coordinator == event.coordinator):
            raise PermissionError("You do not have permission to modify this judge.")
        return obj