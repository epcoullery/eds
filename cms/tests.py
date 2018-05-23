import os

from django.db.models import Sum, F

from django.conf import settings
from django.contrib.auth.models import User
from django.core import mail

from django.test import TestCase, Client
from django.urls import reverse
# Create your tests here.
from cms.models import Domaine, Processus, Module


class PdfTestCase(TestCase):
    fixtures = ['enseignant.json', 'domaine.json', 'processus.json', 'module.json']

    @classmethod
    def setUpTestData(cls):

        User.objects.create_superuser('me', 'me@example.org', 'mepassword')

    def setUp(self):
        self.client = Client()
        self.client.login(username='me', password='mepassword')

    def test_index(self):
        response = self.client.get('')
        self.assertGreater(len(response.content), 200)

    def test_plan_pdf(self):
        response = self.client.get(reverse('plan-pdf'))
        self.assertEqual(
            response['content-disposition'],
            'attachment; filename="EDS_plan_formation.pdf"'
        )
        self.assertEqual(response['content-type'], 'application/pdf')
        self.assertGreater(len(response.content), 200)

    def test_periodes_pdf(self):
        response = self.client.get(reverse('periodes-pdf'))
        self.assertEqual(
            response['content-disposition'],
            'attachment; filename="periode_formation.pdf"'
        )
        self.assertEqual(response['content-type'], 'application/pdf')
        self.assertGreater(len(response.content), 200)

    def test_periode_presentiel(self):
        tot = 0
        for m in Module.objects.all():
            tot += m.total_presentiel
        self.assertEqual(tot, 1200)

    def test_periode_pratique(self):
        tot = Module.objects.aggregate(Sum('pratique_prof'))
        self.assertEqual(tot['pratique_prof__sum'], 1200)

    def test_periode_travail_perso(self):
        tot = Module.objects.aggregate(Sum('travail_perso'))
        self.assertEqual(tot['travail_perso__sum'], 1200)

    def test_periode(self):
        liste = Module.objects.filter(pratique_prof=0)
        context = {}
        for i in range(1, 7):
            semestre = 'sem{}'.format(i)
            context.update({
                semestre: liste.exclude(semestre=0),
                'tot{}'.format(i): liste.aggregate(Sum(F(semestre)))['{}__sum'.format(semestre)]
            })
        print(context)
