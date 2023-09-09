from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenViewBase

from accounts.serializers import RegistrationSerializer, CustomTokenObtainPairSerializer


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