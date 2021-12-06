from django.contrib.auth import authenticate, logout
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
import requests
from rest_framework.views import APIView, View
from oauth2_provider.models import AccessToken
from users.serializers import RegisterSerializer, LoginSerializer

from rest_framework.permissions import IsAuthenticated
from venty.settings import CLIENT_ID, CLIENT_SECRET

UserModel = get_user_model()


# Create your views here.


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            'grant_type': 'password',
            'username': request.validated_data['email'],
            'password': request.validated_data['password'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        }
        r = requests.post('http://127.0.0.1:8000/o/token/', data=data)

        return Response(r.json(), status=r.status_code)


class LoginView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = UserModel.objects.get(email=serializer.data['email'])
        token = AccessToken.objects.get(user_id=user.id)

        response = {
            'message': 'User logged in  successfully',
            'token': token.token,
        }
        status_code = status.HTTP_200_OK

        return Response(response, status=status_code)


class LogoutView(View):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        logout(request)
        return Response()


@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    '''
    {"username": "username", "password": "1234abcd"}
    '''
    r = requests.post(
        'http://127.0.0.1:8000/o/token/',
        data={
            'grant_type': 'password',
            'fullname': request.data['fullname'],
            'username': request.data['username'],
            'password': request.data['password'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        },
    )
    return Response(r.json(), r.status_code)


@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request):
    '''
    {"refresh_token": "<token>"}
    '''
    if (request.data):
        r = requests.post(
            'http://127.0.0.1:8000/o/token/',
            data={
                'grant_type': 'refresh_token',
                'refresh_token': request.data['refresh_token'],
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
            },
        )

        return Response(r.json(), r.status_code)

    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def revoke_token(request):
    '''
    {"token": "<token>"}
    '''
    r = requests.post(
        'http://127.0.0.1:8000/o/revoke_token/',
        data={
            'token': request.data['token'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        },
    )

    if r.status_code == requests.codes.ok:
        return Response({'message': 'token revoked'}, r.status_code)

    return Response(r.json(), r.status_code)

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def register(request):
#     '''
#     {"username": "username", "password": "1234abcd"}
#     '''
#     serializer = CreateUserSerializer(data=request.data)
#
#     if serializer.is_valid():
#         serializer.save()
#
#         r = requests.post('http://127.0.0.1:8000/o/token/',
#                           data={
#                               'grant_type': 'password',
#                               'username': request.data['username'],
#                               'password': request.data['password'],
#                               'client_id': CLIENT_ID,
#                               'client_secret': CLIENT_SECRET,
#                           },
#                           )
#         return Response(r.json(), r.status_code)
#
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
