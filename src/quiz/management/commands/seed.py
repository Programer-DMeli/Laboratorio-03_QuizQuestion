from django.core.management.base import BaseCommand

from quiz.models import Choice, Exam, Question

EXAM_TITLE = "Sonido de los animales"
EXAM_DESCRIPTION = "Examen de prueba con 2 preguntas y 4 opciones cada una."

QUESTIONS = [
    (
        "¿Qué animal dice 'guau'?",
        [
            ("Perro", True),
            ("Gato", False),
            ("Pato", False),
            ("Vaca", False),
        ],
    ),
    (
        "¿Qué animal dice 'miau'?",
        [
            ("Gato", True),
            ("Perro", False),
            ("Pájaro", False),
            ("Caballo", False),
        ],
    ),
]


class Command(BaseCommand):
    help = "Puebla la base de datos con un examen de prueba (idempotente)."

    def handle(self, *args, **options):
        exam, created = Exam.objects.get_or_create(
            title=EXAM_TITLE,
            defaults={"description": EXAM_DESCRIPTION},
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Examen creado: {exam.title}"))
        else:
            exam.description = EXAM_DESCRIPTION
            exam.save()
            self.stdout.write(self.style.WARNING(f"Examen existente reutilizado: {exam.title}"))

        for text, choices in QUESTIONS:
            question, _ = Question.objects.get_or_create(exam=exam, text=text)
            for choice_text, is_correct in choices:
                Choice.objects.get_or_create(
                    question=question,
                    text=choice_text,
                    defaults={"is_correct": is_correct},
                )

        self.stdout.write(self.style.SUCCESS("Seed completado."))