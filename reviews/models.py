from django.conf import settings
from django.db import models

class Review(models.Model):
    # ... другие поля ...
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва'
    )