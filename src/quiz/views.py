from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView

from .forms import ChoiceFormSet, QuestionForm
from .models import Exam, Question


class ExamListView(ListView):
    model = Exam
    context_object_name = 'exams'
    template_name = 'quiz/exam_list.html'

    def get_queryset(self):
        return (
            Exam.objects.annotate(question_count=Count('questions'))
            .order_by('-created_at')
        )


class ExamDetailView(DetailView):
    model = Exam
    context_object_name = 'exam'
    template_name = 'quiz/exam_detail.html'

    def get_queryset(self):
        return Exam.objects.prefetch_related('questions__choices')


class QuestionCreateView(CreateView):
    model = Question
    form_class = QuestionForm
    template_name = 'quiz/question_form.html'

    def get_exam(self):
        return get_object_or_404(Exam, pk=self.kwargs['examen_id'])

    def get_initial(self):
        initial = super().get_initial()
        initial['exam'] = self.get_exam()
        return initial

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['exam'].disabled = True
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['exam'] = self.get_exam()
        if self.request.POST:
            context['choice_formset'] = ChoiceFormSet(self.request.POST)
        else:
            context['choice_formset'] = ChoiceFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['choice_formset']
        if not formset.is_valid():
            return self.render_to_response(context)
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.exam = self.get_exam()
            self.object.save()
            for choice_form in formset:
                if not choice_form.has_changed() or choice_form in formset.deleted_forms:
                    continue
                choice = choice_form.save(commit=False)
                choice.question = self.object
                choice.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('quiz:exam_detail', kwargs={'pk': self.object.exam_id})