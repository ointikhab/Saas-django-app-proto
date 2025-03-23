from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
    
    def validate(self, data):
        if not data.get('email'):
            raise serializers.ValidationError('Email is required.')
        if not data.get('username'):
            raise serializers.ValidationError('Username is required.')
        if User.objects.filter(email=data.get('email')).exists():
            raise serializers.ValidationError('User with this email already exist in our system')
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            raise serializers.ValidationError('Both username and password are required.')

        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError('Invalid credentials.')

        data['user'] = user
        return data
    
class InviteUserSerializer(serializers.Serializer):
    user_email = serializers.EmailField(required=True)
    role = serializers.ChoiceField(choices=['admin', 'employee'])


class AcceptRejectSerializer(serializers.Serializer):
    accept_offer = serializers.BooleanField(required=True)
