import os
import shutil
import tempfile

from django.contrib.auth.models import Group, User
from django.core.files import File
from django.test import TestCase, override_settings
from django.urls import reverse

from cms.models import Module
from.models import IntranetDoc

media_dir = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=media_dir)
class IntranetTests(TestCase):
    fixtures = ['enseignant.json', 'domaine.json', 'processus.json', 'module.json']

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(media_dir)

    def test_document_view(self):
        # Create IntranetDoc instances
        module1 = Module.objects.get(code="M01")
        module2 = Module.objects.get(code="M02")
        doc_etudiant_path = os.path.join(os.path.dirname(__file__), 'test_files', 'doc_etudiant.pdf')
        doc_prof_path = os.path.join(os.path.dirname(__file__), 'test_files', 'doc_prof.pdf')
        with open(doc_etudiant_path, 'rb') as fh:
            IntranetDoc.objects.create(
                doc=File(fh, name='doc_etudiant.pdf'),
                module=module1, published=True, authorization=1
            )
            IntranetDoc.objects.create(
                doc=File(fh, name='doc_etudiant2.pdf'),
                module=module1, published=False, authorization=1
            )
        with open(doc_prof_path, 'rb') as fh:
            IntranetDoc.objects.create(
                doc=File(fh, name='doc_prof.pdf'),
                module=module1, published=True, authorization=2
            )
            IntranetDoc.objects.create(
                doc=File(fh, name='doc_prof2.pdf'),
                module=module2, published=True, authorization=2
            )
        # Create groups and users
        gr_stud1 = Group.objects.create(name='Student_1_year')
        etudiant = User.objects.create(username='student')
        etudiant.groups.add(gr_stud1)
        gr_profs = Group.objects.create(name='prof')
        prof = User.objects.create(username='prof')
        prof.groups.add(gr_profs)

        # Test document visibility by users
        self.client.force_login(etudiant)
        response = self.client.get(reverse('intranet-list', args=[module1.pk]))
        self.assertContains(response, 'doc_etudiant.pdf')
        self.assertNotContains(response, 'doc_etudiant2.pdf')  # Not published
        self.assertNotContains(response, 'doc_prof.pdf')

        self.client.force_login(prof)
        response = self.client.get(reverse('intranet-list', args=[module1.pk]))
        self.assertContains(response, 'doc_etudiant.pdf')
        self.assertNotContains(response, 'doc_etudiant2.pdf')  # Not published
        self.assertContains(response, 'doc_prof.pdf')
        self.assertNotContains(response, 'doc_prof2.pdf')  # Other module
