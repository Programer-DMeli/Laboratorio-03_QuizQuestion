from django import forms
from django.forms import BaseFormSet, formset_factory

from .models import Choice, Exam, Question


class ExamForm(forms.ModelForm):
    """Formulario de examen: usado para alta/edición de Exam y como
    selector de examen en el alta de preguntas."""

    class Meta:
        model = Exam
        fields = ['title', 'description']


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['exam', 'text', 'puntaje']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enunciado de la pregunta'}),
        }


class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['text', 'is_correct']
        widgets = {
            'text': forms.TextInput(attrs={'placeholder': 'Texto de la opción'}),
        }


class BaseChoiceFormSet(BaseFormSet):
    def clean(self):
        if any(self.errors):
            return
        correct_count = 0
        for form in self.forms:
            if self.can_delete and form in self.deleted_forms:
                continue
            if not form.cleaned_data:
                continue
            if form.cleaned_data.get('is_correct'):
                correct_count += 1
        if correct_count != 1:
            raise forms.ValidationError(
                "Cada pregunta debe tener exactamente una opción correcta "
                f"(se encontraron {correct_count}).",
                code='invalid_correct_choices',
            )


ChoiceFormSet = formset_factory(
    ChoiceForm,
    formset=BaseChoiceFormSet,
    extra=4,
    max_num=4,
    validate_max=True,
    can_delete=True,
)