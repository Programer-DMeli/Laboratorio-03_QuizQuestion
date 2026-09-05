from django.test import TestCase
from django.urls import reverse

from .models import Choice, Exam, Question


class ExamViewTests(TestCase):
    def setUp(self):
        self.exam = Exam.objects.create(
            title="Examen de prueba",
            description="Descripción del examen de prueba",
        )

    def test_exam_list_200(self):
        response = self.client.get(reverse('quiz:exam_list'))
        self.assertEqual(response.status_code, 200)

    def test_exam_detail_200(self):
        response = self.client.get(reverse('quiz:exam_detail', kwargs={'pk': self.exam.pk}))
        self.assertEqual(response.status_code, 200)

    def _question_data(self, choices, puntaje=0):
        data = {
            'exam': self.exam.pk,
            'text': '¿Cuál es la capital de Francia?',
            'puntaje': puntaje,
            'form-TOTAL_FORMS': str(len(choices)),
            'form-INITIAL_FORMS': '0',
            'form-MIN_NUM_FORMS': '0',
            'form-MAX_NUM_FORMS': '4',
        }
        for index, (text, is_correct) in enumerate(choices):
            data[f'form-{index}-text'] = text
            data[f'form-{index}-is_correct'] = 'on' if is_correct else ''
        return data

    def test_question_create_valid(self):
        data = self._question_data(
            [('París', True), ('Madrid', False)],
            puntaje=10,
        )
        response = self.client.post(
            reverse('quiz:question_create', kwargs={'examen_id': self.exam.pk}),
            data,
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse('quiz:exam_detail', kwargs={'pk': self.exam.pk}),
        )
        self.assertEqual(Question.objects.count(), 1)
        self.assertEqual(Choice.objects.count(), 2)
        question = Question.objects.get()
        self.assertEqual(question.puntaje, 10)
        self.assertEqual(question.choices.filter(is_correct=True).count(), 1)

    def test_question_create_invalid_two_correct(self):
        data = self._question_data(
            [('París', True), ('Madrid', True)],
        )
        response = self.client.post(
            reverse('quiz:question_create', kwargs={'examen_id': self.exam.pk}),
            data,
        )
        self.assertEqual(response.status_code, 200)
        choice_formset = response.context['choice_formset']
        self.assertFalse(choice_formset.is_valid())
        self.assertTrue(choice_formset.non_form_errors())
        self.assertEqual(Question.objects.count(), 0)
        self.assertEqual(Choice.objects.count(), 0)

    def test_question_create_invalid_zero_correct(self):
        data = self._question_data(
            [('París', False), ('Madrid', False)],
        )
        response = self.client.post(
            reverse('quiz:question_create', kwargs={'examen_id': self.exam.pk}),
            data,
        )
        self.assertEqual(response.status_code, 200)
        choice_formset = response.context['choice_formset']
        self.assertFalse(choice_formset.is_valid())
        self.assertTrue(choice_formset.non_form_errors())
        self.assertEqual(Question.objects.count(), 0)
        self.assertEqual(Choice.objects.count(), 0)