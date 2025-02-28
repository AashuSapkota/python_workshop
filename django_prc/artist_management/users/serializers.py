from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password
from datetime import datetime
import re
from datetime import date


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name', 'last_name', 'email', 'password', 'phone', 'dob', 'gender', 'address', 'created_at', 'updated_at']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},  # Ensure password is write-only
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        password_hash = make_password(password)
        created_at = datetime.now()
        updated_at = datetime.now()
        user = User.objects.create_user(password=password, created_at=created_at, updated_at='', **validated_data)
        return user

    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)

    def validate_phone(self, value):
        if not value.isdigit() or len(value) != 10:
            raise serializers.ValidationError({
                "Status": "Error",
                "Message":"Invalid phone number. Must contain only numbers with 10 digits."
            })
        return value
    
    def validate_email(self, value):
        if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', value):
            raise serializers.ValidationError({
                "Status": "Error",
                "Message":"Invalid Email Format"
            })
        return value