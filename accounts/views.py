from django.shortcuts import render
from rest_framework.generics import GenericAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework_simplejwt.views import TokenViewBase

from accounts.serializers import RegistrationSerializer, CustomTokenObtainPairSerializer, \
    EditProfileSerializer
from accounts.models import User


# Create your views here.
class RegistrationView(GenericAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = (AllowAny,)
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class TokenObtainPairViewCustom(TokenViewBase):
    serializer_class = CustomTokenObtainPairSerializer


class EditProfileView(RetrieveAPIView, UpdateAPIView, GenericViewSet):
    queryset = User.objects.all()
    http_method_names = ['get', 'patch']
    serializer_class = EditProfileSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(request.user)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

