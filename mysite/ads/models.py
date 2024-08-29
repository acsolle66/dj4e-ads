from pyexpat import model
from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator

AUTH_USER_MODEL = get_user_model()


class Ad(models.Model):
    # Ad details
    title = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(2, "Title must be greater than 2 characters")],
    )
    price = models.DecimalField(max_digits=7, decimal_places=2)
    text = models.TextField()
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    # Ad picture
    picture = models.BinaryField(null=True, blank=True, editable=True)
    img_content_type = models.CharField(
        max_length=256, null=True, blank=True, help_text="The MIMEType of the file"
    )
    # Ad timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    comments = models.ManyToManyField(
        "Comment",
        related_name="ad_comments",
        blank=True,
        editable=True,
    )

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.TextField(
        validators=[
            MinLengthValidator(3, "Comment can not be shorter than 3 characters")
        ]
    )

    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        if len(self.text) < 15:
            return self.text
        return self.text[:11] + "..."
