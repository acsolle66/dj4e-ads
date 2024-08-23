from django.test import TestCase
from django.urls import reverse


class HomeViewTest(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.VIEW_URL: str = "/ads"
        cls.URL_NAMESPACE: str = "ads:ads_list"
        cls.USED_TEMPLATE: str = "ads/ads_list_view.html"

    def test_url_exists_at_correct_location(self) -> None:
        self.assertEqual(self.client.get(self.VIEW_URL).status_code, 200)

    def test_namespace_is_registered(self) -> None:
        self.assertEqual(reverse(self.URL_NAMESPACE), self.VIEW_URL)

    def test_used_template(self) -> None:
        self.assertTemplateUsed(self.client.get(self.VIEW_URL), self.USED_TEMPLATE)
