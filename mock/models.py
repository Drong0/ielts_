from django.db import models
from rest_framework.exceptions import ValidationError

from accounts.models import User


class MockWriting(models.Model):
    title = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'mock_writing'


class MockWritingQuestion(models.Model):
    writing_id = models.ForeignKey(MockWriting, on_delete=models.CASCADE, related_name='writing_question')
    question = models.TextField()
    image = models.ImageField(upload_to='writing_questions', blank=True, null=True)
    tips = models.TextField()

    class Meta:
        db_table = 'mock_writing_question'
        ordering = ['id']



class MockWritingResponse(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='writing_response')
    writing_question_id = models.ForeignKey(MockWritingQuestion, on_delete=models.CASCADE,
                                            related_name='writing_response')
    response = models.TextField()

    class Meta:
        db_table = 'mock_writing_response'

    def __str__(self):
        return f'{self.user_id} - {self.writing_question_id}'
