from django.test import Client
from django.test import TestCase
from django.urls import reverse

from project_core.tests import database_population


class CallList(TestCase):
    def setUp(self):
        self._user = database_population.create_management_user()
        self._funding_instrument = database_population.create_funding_instrument()

    def test_load_funding_instrument_add(self):
        c = Client()

        login = c.login(username='unittest_management', password='12345')
        self.assertTrue(login)

        response = c.get(reverse('funding-instrument-add'))
        self.assertEqual(response.status_code, 200)

    def test_load_funding_instruments_list(self):
        c = Client()

        login = c.login(username='unittest_management', password='12345')
        self.assertTrue(login)

        response = c.get(reverse('funding-instruments-list'))
        self.assertEqual(response.status_code, 200)

    def test_load_funding_instrument_update_get(self):
        c = Client()

        login = c.login(username='unittest_management', password='12345')
        self.assertTrue(login)

        response = c.get(reverse('funding-instrument-update', kwargs={'pk': self._funding_instrument.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self._funding_instrument.long_name)

    def test_load_funding_instrument_detail(self):
        c = Client()

        login = c.login(username='unittest_management', password='12345')
        self.assertTrue(login)

        response = c.get(reverse('funding-instrument-detail', kwargs={'pk': self._funding_instrument.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self._funding_instrument.long_name)
