from django.test import TestCase
from django.contrib.admin import site
from ads.models import Ad


class AdModelTest(TestCase):

    def test_fields(self):
        fields = ["title", "price", "text", "owner", "created_at", "updated_at"]
        model_fields = dir(Ad)
        for field in fields:
            self.assertTrue(
                field in model_fields, msg=f"{field} is not defined in the model"
            )

    def test_ad_is_registered(self):
        self.assertTrue(
            site.is_registered(Ad), msg="The model is not registered in admin site"
        )

    def test_string_representation(self):
        ad = Ad(
            title="AdModelTest",
        )

        self.assertEqual(
            ad.title,
            str(ad),
            msg=f"'{ad.text}' != '{str(ad)}' ==> Wrong string representation of model object. Check the Model.__str__()",
        )
