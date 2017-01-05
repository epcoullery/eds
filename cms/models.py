# -*- encoding: utf-8 -*-
'''
Created on 17 nov. 2012

@author: alzo
'''
from django.db import models


# Create your models here.

CHOIX_TYPE_SAVOIR =  (
    ('Savoir','savoir'),
    ('Savoir méthodologique','savoir méthodologique'),
    ('Savoir relationnel','savoir relationnel'),
 )

CHOIX_TYPE_MODULE = (
    ('Spécifique', 'spécifique'),
    ('Transversal', 'transversal'),
)

class Enseignant(models.Model):
    sigle = models.CharField(max_length= 5, blank=True, default='')
    nom = models.CharField(max_length=20, blank=True, default='')
    prenom = models.CharField(max_length=20, blank=True, default='')
    email = models.EmailField(blank=True, default='')
    
    class Meta:
        ordering =('nom',)
        
    def __str__(self):
        return '{0} {1}'.format(self.nom, self.prenom)
    

class Domaine(models.Model):
    code = models.CharField(max_length=20, blank=True)
    libelle = models.CharField(max_length=200, blank=False)
    responsable = models.ForeignKey(Enseignant, null=True, default=None)

    class Meta:
        ordering = ('code',)
        
    def __str__(self):
        return '{0} - {1}'.format(self.code, self.libelle)
    
    def url(self):
        return "<a href='/domaine/{0}'>{1}</a>".format(self.id, self.__str__())


class Processus(models.Model):
    code = models.CharField(max_length=20, blank=True)
    libelle = models.CharField(max_length=200, blank=False)
    domaine = models.ForeignKey(Domaine, null=False)
    description = models.TextField(default='')
    
    
    class Meta:
        ordering = ('code',)
        verbose_name_plural = 'processus'
        
    def __str__(self):
        return '{0} - {1}'.format(self.code, self.libelle)
    
    def url(self):
        return "<a href='/processus/{0}'>{1}</a>".format(self.id, self.__str__())
    

class Module(models.Model):
              
    code = models.CharField(max_length=10, blank=False, default='Code')
    nom = models.CharField(max_length=100, blank=False, default='Nom du module')
    description = models.TextField()
    type = models.CharField(max_length=20, choices= CHOIX_TYPE_MODULE)
    competences = models.ManyToManyField('Competence')
    situation = models.TextField()
    evaluation = models.TextField()
    contenu = models.TextField()
    periode_presentiel = models.IntegerField()
    travail_perso = models.IntegerField()
    pratique_prof = models.IntegerField(default=0)
    didactique = models.TextField(default='')
    evaluation = models.TextField(default='')
    sem1 = models.IntegerField(default=0)
    sem2 = models.IntegerField(default=0)
    sem3 = models.IntegerField(default=0)
    sem4 = models.IntegerField(default=0)
    sem5 = models.IntegerField(default=0)
    sem6 = models.IntegerField(default=0)
    semestre = models.CharField(max_length=15, default='', blank=False)
    processus = models.ForeignKey(Processus, null=False, default=None)
    

    class Meta:
        ordering = ('code',)
        
        
    def __str__(self):
        return '{0} - {1}'.format(self.code, self.nom)
    
    def url(self):
        return "<a href='/module/{0}'>{1}</a>".format(self.id, self.__str__())
    
    def url_code(self):
        return "<a href='/module/{0}'>{1}</a>".format(self.id, self.code)
    
    
class Competence(models.Model):
    code = models.CharField(max_length=20, blank=True)
    libelle = models.CharField(max_length=250, blank=False)
    type = models.CharField(max_length=35, blank=True, default='')
    processus = models.ForeignKey(Processus, null=True, default=None)
    
    class Meta:
        ordering = ('code',)
        verbose_name = 'compétence'
        
    def __str__(self):
        return '{0} - {1}'.format(self.code, self.libelle)
    

    
class SousCompetence(models.Model):
    code = models.CharField(max_length=20, blank=True)
    libelle = models.CharField(max_length=250, blank=False)
    competence = models.ForeignKey(Competence, null=False)
    
    class Meta:
        ordering = ('code',)
        verbose_name = 'sous-compétence'
        
    def __str__(self):
        return '{0} - {1}'.format(self.code, self.libelle)

    
class Ressource(models.Model):
    libelle = models.CharField(max_length=200, blank=False)
    type = models.CharField(max_length=30, choices = CHOIX_TYPE_SAVOIR, default='Savoir')
    module=models.ForeignKey(Module, null=True, default=None)
    
    def __str__(self):
        return '{0}'.format(self.libelle)
    
class Objectif(models.Model):
    libelle = models.CharField(max_length=200, blank=False)
    #type = models.CharField(max_length=30, choices = CHOIX_TYPE_SAVOIR)
    module=models.ForeignKey(Module, null=True, default=None)

    def __str__(self):
        return '{0}'.format(self.libelle)
 
    
class Document(models.Model):
    docfile = models.FileField(upload_to='media')


 

    
    

    

       