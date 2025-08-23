from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'first_name', 'last_name', 'bio', 'profile_picture')
        read_only_fields = ('id',)


CustomUser = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)  # ✅ include token field in response

    class Meta:
        model = CustomUser
        fields = (
            'email', 'password', 'first_name', 'last_name',
            'date_of_birth', 'bio', 'location', 'profile_picture', 'token'
        )

    def create(self, validated_data):
        user = CustomUser.objects.create_user(   # ✅ best practice
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            date_of_birth=validated_data.get('date_of_birth'),
            bio=validated_data.get('bio', ''),
            location=validated_data.get('location', ''),
            profile_picture=validated_data.get('profile_picture')
        )
        # ✅ create a token for this user
        token = Token.objects.create(user=user)
        user.token = token.key
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if not email or not password:
            raise serializers.ValidationError("Email and password are required.")

        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError("Invalid email or password.")

        attrs['user'] = user
        return attrs
    

