from django.db import models


class Exam(models.Model):
    title = models.CharField(max_length=200, verbose_name="Título")
    description = models.TextField(verbose_name="Descripción")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")

    class Meta:
        ordering = ['created_at']
        verbose_name = "Examen"
        verbose_name_plural = "Exámenes"

    def __str__(self):
        return self.title


class Question(models.Model):
    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name="Examen",
    )
    text = models.TextField(verbose_name="Enunciado")
    puntaje = models.PositiveIntegerField(default=0, verbose_name="Puntaje")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")

    class Meta:
        ordering = ['exam', 'created_at']
        verbose_name = "Pregunta"
        verbose_name_plural = "Preguntas"

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='choices',
        verbose_name="Pregunta",
    )
    text = models.CharField(max_length=255, verbose_name="Texto de la opción")
    is_correct = models.BooleanField(default=False, verbose_name="Es correcta")

    class Meta:
        ordering = ['id']
        verbose_name = "Opción"
        verbose_name_plural = "Opciones"

    def __str__(self):
        return self.text