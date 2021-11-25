from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import serializers
from users.models import Account

UserModel = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = Account.objects.create_user(**validated_data)
        return user

    class Meta:
        model = Account
        fields = ('id', 'email', 'password')
        # write_only_fields = ('password',)
        extra_kwargs = {
            'password': {'write_only': True}
        }

# class RegisterSerializer(serializers.ModelSerializer):
#
#     def create(self, validated_data):
#         user = User.objects.create_user(**validated_data)
#         return user
#
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'password')
#         extra_kwargs = {
#             'password': {'write_only': True}
#         }


#
# class LoginSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Account
#         fields = ('email', 'password')
#         extra_kwargs = {
#             'password': {'write_only': True}
#         }
