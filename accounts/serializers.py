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


class EditProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False, allow_null=True)
    password = serializers.CharField(required=False, allow_null=True, write_only=True)
    new_password = serializers.CharField(required=False, allow_null=True, write_only=True)
    new_password_confirm = serializers.CharField(required=False, allow_null=True, write_only=True)

    class Meta:
        model = User
        fields = '__all__'

    def validate(self, a):
        password = a.pop('password', None)
        new_password = a.get('new_password', None)
        new_password_confirm = a.pop('new_password_confirm', None)
        email = a.get('email')

        if email and not password:
            raise serializers.ValidationError({'password': 'Пароль обязательный'})

        if new_password and not password:
            raise serializers.ValidationError({'password': 'Старый пароль обязательный'})

        if new_password and new_password != new_password_confirm:
            raise serializers.ValidationError({'new_password_confirm': 'Подтверждение пароля обязательно'})

        if new_password and not self.instance.check_password(password):
            raise serializers.ValidationError({'password': 'Пароль неверный'})

        if email and not self.instance.check_password(password):
            raise serializers.ValidationError({'password': 'Пароль неверный'})

        return a

    def update(self, instance, validated_data):
        new_password = validated_data.pop('new_password', None)
        instance = super().update(instance, validated_data)
        if new_password:
            instance.set_password(new_password)
            instance.save(update_fields=['password'])

        return instance
