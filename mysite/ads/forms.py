from typing import Any
from django import forms
from ads.models import Ad
from django.core.files.uploadedfile import InMemoryUploadedFile
from utils.humanize import naturalsize
from . import models


class AdForm(forms.ModelForm):
    img_max_upload_limit: int = 2 * 1024 * 1024
    img_max_upload_limit_text: str = naturalsize(img_max_upload_limit)
    img = forms.FileField(
        required=False, label=f"Imge to Upload < {img_max_upload_limit_text}"
    )
    upload_field_name: str = "img"

    class Meta:
        model = Ad
        fields: list[str] = ["title", "price", "text", "img"]

    # Validate the size of the picture
    def clean(self) -> None:
        cleaned_data: dict[str, Any] = super().clean()
        img: Any | None = cleaned_data.get("img")
        if img is None:
            return
        if len(img) > self.img_max_upload_limit:
            self.add_error(
                "img", f"File must be < {self.img_max_upload_limit_text} bytes"
            )

    # Convert uploaded File object to a picture
    def save(self, commit=True):  # -> Any:
        instance: models.Ad = super(AdForm, self).save(commit=False)

        # We only need to adjust picture if it is a freshly uploaded file
        f = instance.img  # Make a copy
        if isinstance(f, InMemoryUploadedFile):
            # Extract data from the form to the model
            bytearr = f.read()
            instance.img_content_type = f.content_type
            instance.img = bytearr  # Overwrite with the actual image data

        if commit:
            instance.save()

        return instance
