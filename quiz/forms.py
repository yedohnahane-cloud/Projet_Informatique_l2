from django import forms
from .models import Quiz
from courses.models import Course


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ["course", "title", "is_published"]
        widgets = {
            "course": forms.Select(attrs={"class": "question-input"}),
            "title": forms.TextInput(attrs={"class": "question-input", "placeholder": "Titre du quiz"}),
            "is_published": forms.CheckboxInput(),
        }