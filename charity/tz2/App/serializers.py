from rest_framework import serializers
from .models import Profile, MedicinesInfo, Medicines
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['phone_number', 'middle_name']


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'profile']

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create_user(**validated_data)
        Profile.objects.create(user=user, **profile_data)
        return user


    # @staticmethod
    # def validate_email(value):
    #     return validate_username(value)


class MedicinesInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicinesInfo
        fields = ['price', 'created', 'available', 'information']


class MedicinesSerializer(serializers.ModelSerializer):
    more_info = MedicinesInfoSerializer()

    class Meta:
        model = Medicines
        fields = ['name', 'more_info']

    def create(self, validated_data):
        med_info_data = validated_data.pop('more_info')
        meds = Medicines.objects.create(**validated_data)
        MedicinesInfo.objects.create(medicine=meds, **med_info_data)
        return meds


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = User
        fields = ['username', 'password']
