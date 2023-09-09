from rest_framework import serializers

from mock.models import MockWriting, MockWritingQuestion, MockWritingResponse


class MockWritingQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MockWritingQuestion
        fields = '__all__'


class MockWritingSerializer(serializers.ModelSerializer):
    writing_question = MockWritingQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = MockWriting
        fields = '__all__'


class MockWritingResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = MockWritingResponse
        fields = '__all__'
