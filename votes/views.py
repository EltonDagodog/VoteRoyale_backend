from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Vote
from .serializers import VoteSerializer
from judges.models import Judge
from events.models import Event
from categories.models import Category
from participants.models import Participant
from categories.serializers import CategorySerializer
from judges.serializers import JudgeSerializer
from events.serializers import EventSerializer
from participants.serializers import ParticipantSerializer



class CoordinatorEventVotesListView(generics.ListAPIView):
    serializer_class = VoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        event_id = self.kwargs['event_id']
        user = self.request.user

        # Check if the user is a coordinator
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Vote.objects.none()

        # Assuming coordinators are linked to events via a coordinator field
        # Adjust this logic based on your actual model relationships
        if hasattr(user, 'coordinator') and event.coordinator.id == user.id:
            return Vote.objects.filter(event_id=event_id)
        return Vote.objects.none()

class EventVotesListView(generics.ListAPIView):
    serializer_class = VoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        event_id = self.kwargs['event_id']
        user = self.request.user
        if hasattr(user, 'judge'):
            return Vote.objects.filter(event_id=event_id, judge=user.judge)
        return Vote.objects.none()

class JudgeDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Endpoint to fetch dashboard data for the judge, including their votes, event, categories, and participants.
        """
        user = request.user
        if not hasattr(user, 'judge'):
            return Response({"error": "User is not a judge."}, status=status.HTTP_403_FORBIDDEN)

        judge = user.judge
        event = judge.event

        # Fetch related data
        categories = Category.objects.filter(event=event)
        participants = Participant.objects.filter(event=event)
        votes = Vote.objects.filter(judge=judge)

        # Serialize data
        categories_serializer = CategorySerializer(categories, many=True)
        participants_serializer = ParticipantSerializer(participants, many=True)
        votes_serializer = VoteSerializer(votes, many=True)

        return Response({
            "judge": JudgeSerializer(judge).data,
            "event": EventSerializer(event).data,
            "participants": participants_serializer.data,
            "categories": categories_serializer.data,
            "votes": votes_serializer.data
        })

class SubmitVoteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, event_id, category_id):
        # Get the judge instance
        try:
            judge = Judge.objects.get(id=request.user.id)
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

        # Verify event and category
        try:
            event = Event.objects.get(id=event_id)
            category = Category.objects.get(id=category_id, event=event)
        except Event.DoesNotExist:
            return Response(
                {"error": "Event not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Category.DoesNotExist:
            return Response(
                {"error": "Category not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Check if category is open for voting
        if category.status != "open":
            return Response(
                {"error": "Category is not open for voting"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if the event deadline has passed
        if timezone.now() > event.date:
            return Response(
                {"error": "The event deadline has passed"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if the judge has already voted for this category
        existing_votes = Vote.objects.filter(judge=judge, category=category)
        if existing_votes.exists():
            return Response(
                {"error": "You have already submitted votes for this category"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get the votes data from the request
        votes_data = request.data.get("votes", [])
        if not votes_data:
            return Response(
                {"error": "No votes provided"},
                status=status.HTTP_400_BAD_REQUEST
            )

        created_votes = []
        for vote_data in votes_data:
            participant_id = vote_data.get("participantId")
            score = vote_data.get("score")
            comments = vote_data.get("comments", "")
            criteria_scores = vote_data.get("criteriaScores", {})

            try:
                participant = Participant.objects.get(id=participant_id, event=event)
            except Participant.DoesNotExist:
                return Response(
                    {"error": f"Participant with ID {participant_id} not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Validate gender match if category is gender-specific
            if category.gender != 'everyone' and participant.gender.lower() != category.gender:
                return Response(
                    {"error": f"Participant {participant.name} does not match the category gender ({category.gender})."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Validate score (assuming frontend sends 0-100 scale, adjust based on category.max_score if different)
            if not isinstance(score, (int, float)) or score < 0 or score > 100:  # Adjusted to 100 to match frontend
                return Response(
                    {"error": f"Invalid score for participant {participant.name}: {score}. Score must be between 0 and 100."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Create the vote
            vote = Vote.objects.create(
                judge=judge,
                participant=participant,
                category=category,
                event=event,
                score=score,
                comments=comments,
                submitted_at=vote_data.get("submittedAt", timezone.now())
            )
            created_votes.append(vote)

        # Serialize the created votes for the response
        serialized_votes = VoteSerializer(created_votes, many=True, context={'request': request}).data
        # Add criteria_scores to the serialized response
        for i, vote in enumerate(serialized_votes):
            vote["criteria_scores"] = votes_data[i].get("criteriaScores", {})

        return Response({
            "message": "Votes submitted successfully",
            "category": category.name,
            "votes": serialized_votes
        }, status=status.HTTP_201_CREATED)