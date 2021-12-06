from django.contrib.auth import authenticate, logout
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
import requests
from rest_framework.views import APIView, View
from oauth2_provider.models import AccessToken, RefreshToken
from users.serializers import RegisterSerializer, LoginSerializer, RefreshSerializer

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
            'username': serializer.validated_data['email'],
            'password': serializer.validated_data['password'],
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

        user = UserModel.objects.get(email=serializer.validated_data['email'])

        token = AccessToken.objects.get(user_id=user.id)
        refresh_token = RefreshToken.objects.get(access_token_id=token.id)

        r = requests.post(
            'http://127.0.0.1:8000/o/token/',
            data={
                'grant_type': 'refresh_token',
                'refresh_token': refresh_token.token,
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
            },
        )

        return Response(r.json(), r.status_code)


class RefreshView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RefreshSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        r = requests.post(
            'http://127.0.0.1:8000/o/token/',
            data={
                'grant_type': 'refresh_token',
                'refresh_token': serializer.validated_data['refresh_token'],
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
            },
        )
        return Response(r.json(), r.status_code)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)
