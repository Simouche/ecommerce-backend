from base_backend.utils import activate_user_over_otp, phone_reconfirmation
from django.contrib.auth.models import Group
from rest_framework import serializers
from rest_framework.fields import ReadOnlyField
from rest_framework.serializers import ModelSerializer

from authentication.models import User, SmsVerification, Profile, City, State, Region


class UserSerializer(ModelSerializer):
    full_name = ReadOnlyField(source='full_name')

    def validate(self, attrs):
        if attrs.get('user_type') == 'D' and not attrs.get('vehicle_type'):
            raise serializers.ValidationError("The delivery guy should have a vehicle")

        return super(UserSerializer, self).validate(attrs)

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        user_type = validated_data.get('user_type')

        if user_type == 'C':
            user.groups.add(Group.objects.get_or_create(name='client')[0])
        elif user_type == 'A':
            user.groups.add(Group.objects.get_or_create(name='admin')[0])
        elif user_type == 'S':
            user.groups.add(Group.objects.get_or_create(name='staff')[0])

        return user

    class Meta:
        model = User
        fields = ['id', 'phones', 'email', 'first_name', 'last_name', 'user_type', 'password',
                  'username', 'full_name']
        extra_kwargs = {
            "password": {"write_only": True},
            'photo': {'required': False},
            'id': {'read_only': True},
        }


class SmsConfirmationSerializer(ModelSerializer):
    otp_code = serializers.CharField(required=False)
    phone = serializers.CharField(required=False)

    def validate(self, attrs):
        if not attrs.get('otp_code') and not attrs.get('phone'):
            raise serializers.ValidationError("You should provide either a code or a phone number")

        return super(SmsConfirmationSerializer, self).validate(attrs)

    def create(self, validated_data):
        return None

    def update(self, instance, validated_data):
        return None

    def activate(self):
        self.is_valid(raise_exception=True)
        return activate_user_over_otp(self.validated_data.get('otp_code'))

    def resend(self):
        self.is_valid(raise_exception=True)
        try:
            record = SmsVerification.objects.get(number='+' + self.validated_data.get('phone'), confirmed=False)
            phone_reconfirmation(record)
            return True
        except SmsVerification.DoesNotExist:
            return False


class ProfileSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ['id', 'user', 'photo', 'address', 'city', 'birth_date', 'gender']
        extra_kwargs = {
            'id': {
                'read_only': True,
            }
        }


class CitySerializer(ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'code_postal', 'state']
        extra_kwargs = {
            'id': {
                'read_only': True,
            }
        }


class StateSerializer(ModelSerializer):
    cities = CitySerializer(many=True)

    class Meta:
        model = State
        fields = ['id', 'matricule', 'code_postal', 'region', 'cities']
        extra_kwargs = {
            'id': {
                'read_only': True,
            }
        }


class RegionSerializer(ModelSerializer):
    states = StateSerializer(many=True)

    class Meta:
        model = Region
        fields = ['id', 'name', 'states']
        extra_kwargs = {
            'id': {
                'read_only': True,
            }
        }
