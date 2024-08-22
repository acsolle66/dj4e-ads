from django.test import TestCase
from . import config


class HomeTemplatesTest(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.VIEW_URL: str = "/"

    def test_template_content(self) -> None:
        self.assertContains(self.client.get(self.VIEW_URL), "/ads")
