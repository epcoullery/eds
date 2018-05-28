"""
Created on 17 nov. 2012

@author: alzo
"""

from django.db import models
from django.utils.html import format_html

from tinymce import models as tinymce_models


CHOIX_TYPE_SAVOIR = (
    ('Savoir', 'savoir'),
    ('Savoir-faire méthodologique et technique', 'savoir méthodologique'),
    ('Savoir-faire relationnel', 'savoir relationnel'),
)


CHOIX_TYPE_MODULE = (
    ('Spécifique', 'spécifique'),
    ('Transversal', 'transversal'),
)


class Enseignant(models.Model):
    sigle = models.CharField(max_length=5, blank=True)
    nom = models.CharField(max_length=20, blank=True)
    prenom = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    class Meta:
        ordering = ('nom',)

    def __str__(self):
        return '{0} {1}'.format(self.nom, self.prenom)
    
    def descr(self):
        return '{0} (<a href="mailto:{1}">{2}</A>)'.format(self.__str__(), self.email, self.email)

    def descr_pdf(self):
        return '{0} ({1})'.format(self.__str__(), self.email)
    
    
class Domaine(models.Model):
    code = models.CharField(max_length=20, blank=True)
    nom = models.CharField(max_length=200, blank=False)
    responsable = models.ForeignKey(Enseignant, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ('code', )

    def __str__(self):
        return '{0} - {1}'.format(self.code, self.nom)
    
    def url(self):
        return format_html('<a href="/domaine/{0}/">{1}</a>', self.pk, str(self))


class Processus(models.Model):
    code = models.CharField(max_length=20, blank=True)
    nom = models.CharField(max_length=200, blank=False)
    domaine = models.ForeignKey(Domaine, null=False, on_delete=models.PROTECT)
    description = models.TextField()

    class Meta:
        ordering = ('code',)
        verbose_name_plural = 'processus'

    def __str__(self):
        return '{0} - {1}'.format(self.code, self.nom)
    
    def url(self):
        return format_html('<a href="/processus/{0}/">{1}</a>', self.pk, str(self))
    

class Module(models.Model):
    code = models.CharField(max_length=10, blank=False, default='Code')
    nom = models.CharField(max_length=100, blank=False, default='Nom du module')
    type = models.CharField(max_length=20, choices=CHOIX_TYPE_MODULE)
    situation = models.TextField()
    evaluation = models.TextField()
    contenu = models.TextField()
    travail_perso = models.IntegerField(verbose_name='Travail personnel')
    pratique_prof = models.IntegerField(default=0, verbose_name='Pratique prof.')
    didactique = models.TextField()
    sem1 = models.IntegerField(default=0)
    sem2 = models.IntegerField(default=0)
    sem3 = models.IntegerField(default=0)
    sem4 = models.IntegerField(default=0)
    sem5 = models.IntegerField(default=0)
    sem6 = models.IntegerField(default=0)
    semestre = models.CharField(max_length=15)
    processus = models.ForeignKey(Processus, on_delete=models.PROTECT)
    
    didactique_published = models.BooleanField(default=False)
    evaluation_published = models.BooleanField(default=False)
    contenu_published = models.BooleanField(default=False)

    class Meta:
        ordering = ('code',)

    def __str__(self):
        return '{0} - {1}'.format(self.code, self.nom)
    
    def url(self):
        return format_html('<a href="/module/{0}/">{1}</a>', self.pk, str(self))
    
    def url_code(self):
        return format_html('<a href="/module/{0}/" title="{2}">{1}</a>', self.pk, self.code, self.nom)

    @property
    def total_presentiel(self):
        return self.sem1 + self.sem2 + self.sem3 + self.sem4 + self.sem5 + self.sem6 - self.pratique_prof


class Competence(models.Model):
    code = models.CharField(max_length=20, blank=True)
    nom = models.CharField(max_length=250, blank=False)
    type = models.CharField(max_length=35, blank=True)
    module = models.ForeignKey(Module, null=True, blank=True, on_delete=models.SET_NULL)
    proces_eval = models.ForeignKey(Processus, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ('code',)
        verbose_name = 'compétence'

    def __str__(self):
        return '{0} - {1}'.format(self.code, self.nom)
    
    
class SousCompetence(models.Model):
    code = models.CharField(max_length=20, blank=True)
    nom = models.CharField(max_length=250, blank=False)
    competence = models.ForeignKey(Competence, null=False, on_delete=models.PROTECT)

    class Meta:
        ordering = ('code',)
        verbose_name = 'sous-compétence'

    def __str__(self):
        return '{0} - {1}'.format(self.code, self.nom)

    
class Ressource(models.Model):
    nom = models.CharField(max_length=200, blank=False)
    type = models.CharField(max_length=50, choices=CHOIX_TYPE_SAVOIR, default='Savoir')
    module = models.ForeignKey(Module, null=True, blank=True, on_delete=models.PROTECT)
    
    def __str__(self):
        return '{0}'.format(self.nom)


class Objectif(models.Model):
    nom = models.CharField(max_length=200, blank=False)
    module = models.ForeignKey(Module, null=True, blank=True, on_delete=models.PROTECT)

    def __str__(self):
        return '{0}'.format(self.nom)
 
    
class Concept(models.Model):
    titre = models.CharField(max_length=128, blank=True)
    texte = tinymce_models.HTMLField(blank=True)
    published = models.BooleanField(default=False)
    
    def __str__(self):
        return self.titre


class UploadDoc(models.Model):
    docfile = models.FileField(upload_to='doc')
    titre = models.CharField(max_length=100, blank=False)
    published = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'UploadDoc'

    def __str__(self):
        return self.titre
