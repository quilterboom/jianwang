from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, MistakeRecord


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        UserProfile.objects.create(user=user)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    no_mistake_days = serializers.IntegerField(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'mistake_count', 'no_mistake_days', 'last_mistake_date']


class MistakeRecordSerializer(serializers.ModelSerializer):
    investment_type_display = serializers.CharField(source='get_investment_type_display', read_only=True)
    created_at_formatted = serializers.DateTimeField(source='created_at', format='%Y-%m-%d %H:%M:%S', read_only=True)

    class Meta:
        model = MistakeRecord
        fields = ['id', 'investment_type', 'investment_type_display', 'reason', 'created_at', 'created_at_formatted']
        read_only_fields = ['created_at']
