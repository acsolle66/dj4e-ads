from django.test import TestCase


class HomeTemplatesTest(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.VIEW_URL: str = "/"

    def test_template_content(self) -> None:
        self.assertContains(self.client.get(self.VIEW_URL), "/ads")
