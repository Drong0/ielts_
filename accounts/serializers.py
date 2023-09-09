from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainSerializer, TokenObtainPairSerializer

from accounts.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'phone', 'first_name', 'last_name', 'password',
                  'password_confirm',)

    def run_validation(self, data):
        email = data.get('email')
        inactive_user = User.objects.filter(email=email, is_active=False, email_approved=False, is_staff=False)

        if inactive_user.exists():
            inactive_user.delete()

        return super().run_validation(data=data)

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm')

        if password != password_confirm:
            raise serializers.ValidationError({
                'password': _('Пароли должны совпадать')
            })

        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        instance = super().create(validated_data)
        instance.set_password(password)
        instance.save()

        return instance


class CustomTokenObtainSerializer(TokenObtainSerializer):
    default_error_messages = {
        'no_active_account': 'Wrong password or username. Try again or click Forgot password to reset it'
    }


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer, CustomTokenObtainSerializer):
    pass
