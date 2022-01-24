import json

from django.contrib.auth import logout
from rest_framework import status, permissions
from rest_framework.response import Response

from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
import requests
from rest_framework.views import APIView, View
from oauth2_provider.models import AccessToken, RefreshToken
from users.serializers import RegisterSerializer, LoginSerializer, RefreshSerializer, CurrentUserSerializer

from rest_framework.permissions import IsAuthenticated
from venty.settings import CLIENT_ID, CLIENT_SECRET

UserModel = get_user_model()


# Create your views here.
URL = 'https://venty-be.herokuapp.com/o/token/'
# URL = 'http://127.0.0.1:8000/o/token/'

class RegisterView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = {
            'grant_type': 'password',
            'username': serializer.validated_data['email'],
            'password': serializer.validated_data['password'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        }
        try:
            r = requests.post(URL, data=data)
            return Response(r.json(), status=r.status_code)
        except:
            user.delete()
            return Response(status=status.HTTP_400_BAD_REQUEST)




class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = UserModel.objects.get(email=serializer.validated_data['email'])
        try:
            token = AccessToken.objects.get(user_id=user.id)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        refresh_token = RefreshToken.objects.get(access_token_id=token.id)
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token.token,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        }
        try:
            r = requests.post(URL, data=data)
            return Response(r.json(), r.status_code)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class RefreshView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RefreshSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = {
                   'grant_type': 'refresh_token',
                   'refresh_token': serializer.validated_data['refresh_token'],
                   'client_id': CLIENT_ID,
                   'client_secret': CLIENT_SECRET,
               },
        r = requests.post(URL, data=data)

        return Response(r.json(), r.status_code)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class CurrentUserView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        token = request.headers.get('Authorization').split()[1]
        user_id = AccessToken.objects.get(token=token).user_id
        queryset = UserModel.objects.get(id=user_id)

        return Response(data=CurrentUserSerializer(queryset).data, status=status.HTTP_200_OK)
