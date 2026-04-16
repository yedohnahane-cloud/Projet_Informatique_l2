from django import forms
from .models import Subject, Course


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ["title", "description", "is_published"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "cours-form"}),
            "description": forms.Textarea(attrs={"class": "cours-form", "rows": 5}),
            "is_published": forms.CheckboxInput(),
        }


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["subject", "order", "title", "content", "pdf_file", "is_published"]
        widgets = {
            "subject": forms.Select(attrs={"class": "cours-form"}),
            "order": forms.NumberInput(attrs={"class": "cours-form"}),
            "title": forms.TextInput(attrs={"class": "cours-form"}),
            "content": forms.Textarea(attrs={"class": "cours-form", "rows": 6}),
            "pdf_file": forms.ClearableFileInput(attrs={"class": "cours-form"}),
            "is_published": forms.CheckboxInput(),
        }