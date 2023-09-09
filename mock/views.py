import openai
from django.shortcuts import render
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from mock.models import MockWriting, MockWritingResponse
from mock.serializers import MockWritingSerializer, MockWritingResponseSerializer
import random


# Create your views here.
class RandomMockWritingView(RetrieveAPIView):
    queryset = MockWriting.objects.all()
    serializer_class = MockWritingSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        # Randomly select one MockWriting object

        self.object = random.choice(self.get_queryset())

        # Serialize and return the object
        serializer = self.get_serializer(self.object)
        return Response(serializer.data)


class MockWritingResponseView(CreateAPIView):
    queryset = MockWritingResponse.objects.all()
    serializer_class = MockWritingResponseSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Get the data from the request
        data = request.data
        data['user_id'] = request.user.id

        # Create a serializer instance
        serializer = self.get_serializer(data=data)

        # Validate the data
        serializer.is_valid(raise_exception=True)

        # Save the data
        serializer.save()

        # Return the response
        return Response(serializer.data)

