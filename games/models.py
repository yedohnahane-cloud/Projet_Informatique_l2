from django.db import models


class Game(models.Model):
    CATEGORY_CHOICES = [
        ("java", "Java"),
        ("algorithm", "Algorithmique"),
        ("oop", "POO"),
        ("logic", "Logique"),
        ("general", "Général"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    source_url = models.URLField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="general")
    is_active = models.BooleanField(default=True)
    thumbnail = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title