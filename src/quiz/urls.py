from django.urls import path

from .views import ExamDetailView, ExamListView, QuestionCreateView

app_name = 'quiz'

urlpatterns = [
    path('', ExamListView.as_view(), name='exam_list'),
    path('examenes/<int:pk>/', ExamDetailView.as_view(), name='exam_detail'),
    path(
        'examenes/<int:examen_id>/questions/new/',
        QuestionCreateView.as_view(),
        name='question_create',
    ),
]