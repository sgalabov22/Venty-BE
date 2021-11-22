from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

import requests

from venty.settings import CLIENT_ID, CLIENT_SECRET
from users.serializers import CreateUserSerializer

# Create your views here.
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    '''
    {"username": "username", "password": "1234abcd"}
    '''
    serializer = CreateUserSerializer(data=request.data) 

    if serializer.is_valid():
        serializer.save() 

        r = requests.post('http://127.0.0.1:8000/o/token/', 
            data = {
                'grant_type': 'password',
                'username': request.data['username'],
                'password': request.data['password'],
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
            },
        )
        return Response(r.json(), r.status_code)
    
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    '''
    {"username": "username", "password": "1234abcd"}
    '''
    r = requests.post(
    'http://127.0.0.1:8000/o/token/', 
        data = {
            'grant_type': 'password',
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
            data = {
                'grant_type': 'refresh_token',
                'refresh_token': request.data['refresh_token'],
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
            },
        )
    
        return Response(r.json(), r.status_code)
    
    return Response(status = status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def revoke_token(request):
    '''
    {"token": "<token>"}
    '''
    r = requests.post(
        'http://127.0.0.1:8000/o/revoke_token/', 
        data = {
            'token': request.data['token'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        },
    )

    if r.status_code == requests.codes.ok:
        return Response({'message': 'token revoked'}, r.status_code)

    return Response(r.json(), r.status_code)