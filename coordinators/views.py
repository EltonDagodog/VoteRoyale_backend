from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken # type: ignore
from django.contrib.auth import authenticate
from coordinators.models import Coordinator
from coordinators.serializers import CoordinatorRegistrationSerializer, CoordinatorSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def coordinator_register(request):
    serializer = CoordinatorRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(CoordinatorSerializer(user).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def coordinator_login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(request, email=email, password=password)

    if user is None or user.role != 'coordinator':
        return Response({'error': 'Invalid credentials or not a coordinator'}, status=status.HTTP_401_UNAUTHORIZED)

    refresh = RefreshToken.for_user(user)
    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user': CoordinatorSerializer(user).data
    })