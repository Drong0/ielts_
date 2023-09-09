from mock import views
from django.urls import path

urlpatterns = [
    path('writing/', views.RandomMockWritingView.as_view(), name='random_mock_writing'),
    path('writing/save/', views.MockWritingResponseView.as_view(), name='save_mock_writing'),
]
