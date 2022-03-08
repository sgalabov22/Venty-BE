from django.contrib.auth import authenticate, get_user_model
from oauth2_provider.models import AccessToken
from rest_framework import serializers
from users.models import Account

UserModel = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = Account.objects.create_user(**validated_data)
        authenticate(email=validated_data['email'], password=validated_data['password'])
        return user

    class Meta:
        model = Account
        fields = ('fullname', 'id', 'email', 'password', 'profile_picture')
        write_only_fields = ('password',)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                {
                    "error": 'A user with this email and password is not found.'
                }
            )

        return {
            'email': user.email,
        }


class RefreshSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(max_length=255)



class CurrentUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        exclude = ('password',)
