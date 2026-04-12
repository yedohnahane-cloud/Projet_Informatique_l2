from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


def validate_amu_email(email):
    email = email.lower().strip()

    if not (
        email.endswith("@etu.univ-amu.fr")
        or email.endswith("@univ-amu.fr")
    ):
        raise ValidationError(
            "Veuillez utiliser une adresse email universitaire AMU."
        )


class User(AbstractUser):
    ROLE_CHOICES = (
        ("student", "Étudiant"),
        ("teacher", "Professeur"),
    )

    username = None

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default="student"
    )

    email = models.EmailField(
        unique=True,
        validators=[validate_amu_email]
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return self.email