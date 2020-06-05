from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

from .serializers import RegistrationSerializer, AccountPropertiesSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


@api_view(['POST', ])
@permission_classes((AllowAny, ))
def registration_view(request):
    serializer = RegistrationSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        user = serializer.save()
        data['response'] = 'succesfully registered a new user'
        data['username'] = user.username
        data['email'] = user.email
        data['token'] = Token.objects.get(user=user).key
    else:
        data = serializer.errors
    return Response(data)


@api_view(['GET', ])
@permission_classes((IsAuthenticated, ))
def account_properties_view(request):
    try:
        user = request.user
    except User.UserNotFound:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = AccountPropertiesSerializer(user)
    return Response(serializer.data)


@api_view(['PUT', ])
@permission_classes((IsAuthenticated, ))
def update_account_view(request):
    try:
        user = request.user
    except User.UserNotFound:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = AccountPropertiesSerializer(user, request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'success' : 'update successful'})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)