# pylint: disable=C0103

from django.test import (
    SimpleTestCase,
    TestCase,
    override_settings,
)
from django.urls import path, reverse

from console import console

from vb_baseapp.views import (
    custom_400_error,
    custom_403_error,
    custom_404_error,
    custom_500_error,
)

console = console(source=__name__)

urlpatterns = [
    path('500/', custom_500_error),
    path('403/', custom_403_error),
    path('400/', custom_400_error),
    path('404/', custom_404_error),
]

handler400 = custom_400_error
handler403 = custom_403_error
handler404 = custom_404_error
handler500 = custom_500_error


class ViewTestCase(TestCase):
    def test_index_view(self):
        response = self.client.get(reverse('vb_baseapp:index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome to Django')
        environment_name = response.context.get('DJANGO_ENV', None)
        self.assertTrue(environment_name in ['test', 'travis'])

        templates = list(map(lambda t: t.name, response.templates))
        self.assertTrue('index.html' in templates)


@override_settings(ROOT_URLCONF=__name__)
class CustomServerErrorViewTests(SimpleTestCase):
    def test_404_error_view(self):
        response = self.client.get('/this/url/does/not/exists/')

        self.assertEqual(response.status_code, 404)

        templates = list(map(lambda t: t.name, response.templates))
        self.assertTrue('custom_errors/404.html' in templates)

    def test_500_error_view(self):
        response = self.client.get('/500/')
        self.assertEqual(response.status_code, 500)
        templates = list(map(lambda t: t.name, response.templates))
        self.assertTrue('custom_errors/500.html' in templates)

    def test_403_error_view(self):
        response = self.client.get('/403/')
        self.assertEqual(response.status_code, 403)
        templates = list(map(lambda t: t.name, response.templates))
        self.assertTrue('custom_errors/403.html' in templates)

    def test_400_error_view(self):
        response = self.client.get('/400/')
        self.assertEqual(response.status_code, 400)
        templates = list(map(lambda t: t.name, response.templates))
        self.assertTrue('custom_errors/400.html' in templates)
