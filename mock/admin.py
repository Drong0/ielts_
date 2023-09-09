from django.contrib import admin
from django.contrib.admin import TabularInline

# Register your models here.
from mock.models import MockWriting, MockWritingQuestion, MockWritingResponse


class MockWritingQuestionInline(TabularInline):
    model = MockWritingQuestion
    extra = 1


@admin.register(MockWriting)
class MockWritingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')

    inlines = [
        MockWritingQuestionInline,
    ]

@admin.register(MockWritingResponse)
class MockWritingResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'writing_question_id', 'response')

