from pyexpat import model
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator

AUTH_USER_MODEL = get_user_model()


class Ad(models.Mode):
    title = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(2, "Title must be greater than 2 characters")],
    )
    price = models.DecimalField(max_digits=7, decimal_places=2)
    text = models.TextField()
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE())
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
