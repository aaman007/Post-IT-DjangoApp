from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated

from .serializers import RegistrationSerializer, AccountPropertiesSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.views import APIView


@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def registration_view(request):
    data = {}
    email = request.data.get('email','0')
    username = request.data.get('username', '0')

    if username_exist(username):
        data['response'] = 'Error'
        data['error_message'] = 'Username is already in use'
        return Response(data)

    serializer = RegistrationSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        data['response'] = 'succesfully registered a new user'
        data['pk'] = user.pk
        data['username'] = user.username
        data['email'] = user.email
        data['token'] = Token.objects.get(user=user).key
    else:
        data = serializer.errors
    return Response(data)


def username_exist(username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return False
    return True


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


# Login View
class ObtainAuthTokenView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):
        context = {}

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            try:
                token = Token.objects.get(user=user)
            except:
                token = Token.objects.create(user=user)
            context['response'] = 'successfully authenticated'
            context['pk'] = user.pk
            context['username'] = user.pk
            context['token'] = token.key
        else:
            context['response'] = 'Error'
            context['error_message'] = 'Invalid Credentials'
        return Response(context)