from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff']
        read_only_fields = ['id', 'is_staff']


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150, required=True)
    first_name = serializers.CharField(max_length=150, allow_blank=True, required=False)
    last_name = serializers.CharField(max_length=150, allow_blank=True, required=False)
    email = serializers.EmailField(required=True, max_length=254)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password_confirmation = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'password_confirmation',
        ]

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Користувач із такою електронною поштою вже існує.")
        return value

    def validate(self, data):
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError("Password does not match")
        password = data['password']
        if len(password) < 8:
            raise serializers.ValidationError("At least 8 characters required")
        if not any(char.isalpha() for char in password):
            raise serializers.ValidationError("At least one character must be alphanumeric.")
        if not any(char.isdigit() for char in password):
            raise serializers.ValidationError("At least one character must be digits.")

        return data

    def create(self, validated_data):
        validated_data.pop('password_confirmation')

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        return user
