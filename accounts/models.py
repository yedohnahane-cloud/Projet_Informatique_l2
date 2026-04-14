from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.contrib.auth.models import BaseUserManager

def validate_amu_email(email):
    email = email.lower().strip()

    if not (
        email.endswith("@etu.univ-amu.fr")
        or email.endswith("@univ-amu.fr")
    ):
        raise ValidationError(
            "Veuillez utiliser une adresse email universitaire AMU."
        )

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("L'utilisateur doit avoir un email")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)
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
    objects = UserManager()

    def __str__(self):
        return self.email
 