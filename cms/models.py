# -*- encoding: utf-8 -*-
'''
Created on 17 nov. 2012

@author: alzo
'''
from django.db import models
from django.http.response import HttpResponse
from django.conf import settings

from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph, Spacer, PageBreak, Table, TableStyle, Image
from reportlab.graphics.shapes import Line
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle as PS
style_8_c = PS(name='CORPS', fontName='Helvetica', fontSize=6, alignment = TA_CENTER)
style_normal = PS(name='CORPS', fontName='Helvetica', fontSize=8, alignment = TA_LEFT)
style_bold = PS(name='CORPS', fontName='Helvetica-Bold', fontSize=10, alignment = TA_LEFT)
style_title = PS(name='CORPS', fontName='Helvetica', fontSize=12, alignment = TA_LEFT)
style_adress = PS(name='CORPS', fontName='Helvetica', fontSize=10, alignment = TA_LEFT, leftIndent=300)
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
    
    def descr(self):
        return '{0} (<A HREF="{1}">{3}</A>)'.format(self.__str__(), self.email, self.email)
 
    
class SVG_Domaine:
    compteur = 0
    x = 30
    y = 10
    width = 200
    svg = '<rect x="20" y="{0}" rx="5" ry="5" width="60" height="{1}" fill="{3}" stroke="black" stroke-width="2" />'
    txt = '<text x="25" y="{0}" style="stroke:#000000;font-size:12;">{1}</text>'
    
    def get_svg(self):
        return '{0}{1}'.format(self.svg, self.txt)
    
    def __init__(self, domaine):
        SVG_Domaine.compteur += 1
        self.svg = self.svg.format(20, 100, settings.DOMAINE_COULEUR[domaine.code])
        self.txt = self.txt.format(20, domaine.__str__())
        
    
    
class Domaine(models.Model):
    code = models.CharField(max_length=20, blank=True)
    nom = models.CharField(max_length=200, blank=False)
    responsable = models.ForeignKey(Enseignant, null=True, default=None)
    
    class Meta:
        ordering = ('code',)
        
    def __str__(self):
        return '{0} - {1}'.format(self.code, self.nom)
    
    def url(self):
        return "<a href='/domaine/{0}'>{1}</a>".format(self.id, self.__str__())

    def svg(self):
        svg = '<rect x="20" y="{0}" rx="5" ry="5" width="200" height="{1}" fill="{2}" stroke="black" stroke-width="1" />'
        txt = '<text x="25" y="{0}" style="stroke:#000000;font-size:10;">{1}</text>'
        
        return svg.format(20, 100, settings.DOMAINE_COULEURS[self.code]) + txt.format(50, self.__str__())
        
    


class Processus(models.Model):
    code = models.CharField(max_length=20, blank=True)
    nom = models.CharField(max_length=200, blank=False)
    domaine = models.ForeignKey(Domaine, null=False)
    description = models.TextField(default='')
    
    
    class Meta:
        ordering = ('code',)
        verbose_name_plural = 'processus'
        
    def __str__(self):
        return '{0} - {1}'.format(self.code, self.nom)
    
    def url(self):
        return "<a href='/processus/{0}'>{1}</a>".format(self.id, self.__str__())
    

class Module(models.Model):
              
    code = models.CharField(max_length=10, blank=False, default='Code')
    nom = models.CharField(max_length=100, blank=False, default='Nom du module')
    type = models.CharField(max_length=20, choices= CHOIX_TYPE_MODULE)
    situation = models.TextField()
    evaluation = models.TextField()
    contenu = models.TextField()
    periode_presentiel = models.IntegerField()
    travail_perso = models.IntegerField()
    pratique_prof = models.IntegerField(default=0)
    didactique = models.TextField()
    evaluation = models.TextField()
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
        return "<a href='/module/{0}' title='{2}'>{1}</a>".format(self.id, self.code, self.nom)
    
    
class Competence(models.Model):
    code = models.CharField(max_length=20, blank=True)
    nom = models.CharField(max_length=250, blank=False)
    type = models.CharField(max_length=35, blank=True, default='')
    module = models.ForeignKey(Module, null=True, default=None)
    
    class Meta:
        ordering = ('code',)
        verbose_name = 'compétence'
        
    def __str__(self):
        return '{0} - {1}'.format(self.code, self.nom)
    

    
class SousCompetence(models.Model):
    code = models.CharField(max_length=20, blank=True)
    nom = models.CharField(max_length=250, blank=False)
    competence = models.ForeignKey(Competence, null=False)
    
    class Meta:
        ordering = ('code',)
        verbose_name = 'sous-compétence'
        
    def __str__(self):
        return '{0} - {1}'.format(self.code, self.nom)

    
class Ressource(models.Model):
    nom = models.CharField(max_length=200, blank=False)
    type = models.CharField(max_length=30, choices = CHOIX_TYPE_SAVOIR, default='Savoir')
    module=models.ForeignKey(Module, null=True, default=None)
    
    def __str__(self):
        return '{0}'.format(self.nom)
    
class Objectif(models.Model):
    nom = models.CharField(max_length=200, blank=False)
    module=models.ForeignKey(Module, null=True, default=None)

    def __str__(self):
        return '{0}'.format(self.nom)
 
    
class Document(models.Model):
    docfile = models.FileField(upload_to='media')


 
class PDFResponse(HttpResponse):
    
    def __init__(self, filename, title='', portrait=True):
        HttpResponse.__init__(self, content_type='application/pdf')
        self['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
        self['Content-Type'] = 'charset=utf-8'
        self.story = []
        image = Image(settings.MEDIA_ROOT + '/media/header.png', width=480, height=80)
        image.hAlign = TA_LEFT
        
        self.story.append(image)
        #self.story.append(Spacer(0,1*cm))
        
        data = [['Filières EDS', title]]
        if portrait:
            t =  Table(data, colWidths=[8*cm,8*cm])
        else:
            t =  Table(data, colWidths=[11*cm,11*cm])
        t.setStyle(TableStyle([ ('ALIGN',(0,0),(0,0),'LEFT'),
                                ('ALIGN',(1,0),(-1,-1),'RIGHT'),
                                ('LINEABOVE', (0,0) ,(-1,-1), 0.5, colors.black),
                                ('LINEBELOW', (0,-1),(-1,-1), 0.5, colors.black),
                            ]))
        t.hAlign = TA_LEFT
        self.story.append(t)
        
        
    
class MyDocTemplate(SimpleDocTemplate):
    
    def __init__(self, name):
        SimpleDocTemplate.__init__(self, name, pagesize=A4, topMargin=0*cm)
        self.fileName = name
        self.PAGE_WIDTH = A4[0]
        self.PAGE_HEIGHT = A4[1]
        self.CENTRE_WIDTH = self.PAGE_WIDTH/2.0
        self.CENTRE_HEIGHT = self.PAGE_HEIGHT/2.0
        
        
    def beforePage(self):
        # page number
        self.canv.saveState()
        self.canv.setFontSize(8)
        self.canv.drawCentredString(self.CENTRE_WIDTH,1*cm,"Page : " + str(self.canv.getPageNumber()))
        self.canv.restoreState()
        
        
    
class MyDocTemplateLandscape(SimpleDocTemplate):
    
    def __init__(self, name):
        SimpleDocTemplate.__init__(self, name, pagesize=landscape(A4), topMargin=0*cm, leftMargin=2*cm)
        self.fileName = name
        self.PAGE_WIDTH = A4[1]
        self.PAGE_HEIGHT = A4[0]
        self.CENTRE_WIDTH = self.PAGE_WIDTH/2.0
        self.CENTRE_HEIGHT = self.PAGE_HEIGHT/2.0
        
    def beforePage(self):
        # page number
        self.canv.saveState()
        self.canv.setFontSize(8)
        self.canv.drawCentredString(self.CENTRE_WIDTH,1*cm,"Page : " + str(self.canv.getPageNumber()))
        self.canv.restoreState()
    
    

       