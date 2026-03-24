from django import forms
from .models import User


class SignUpForm(forms.ModelForm):
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput
    )
    confirm_password = forms.CharField(
        label="Confirmer le mot de passe",
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password"]

    def clean_email(self):
        email = self.cleaned_data.get("email", "").lower().strip()

        if not email.endswith("@etu.univ-amu.fr"):
            raise forms.ValidationError(
                "L'inscription est réservée aux étudiants avec une adresse @etu.univ-amu.fr."
            )

        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Les mots de passe ne correspondent pas.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = "student"
        user.set_password(self.cleaned_data["password"])

        if commit:
            user.save()

        return user