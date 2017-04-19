# -*- encoding: utf-8 -*-
'''
Created on 17 nov. 2012

@author: alzo
'''
from .models import (Processus, Module, Domaine, Competence, SousCompetence, Document,
                    UploadDoc)

from django import forms

from django.contrib import admin
from _collections_abc import __all__
#from django.forms import Textarea, TextInput

from tinymce.widgets import TinyMCE



class DocumentAdminForm(forms.ModelForm):
    
    class Meta:
        model = Document
        fields = ('titre', 'texte','published')
        
        widgets = {
            'texte': TinyMCE(attrs={'cols': 120, 'rows': 30}),
            }
        
  
class ProcessusAdminForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(ProcessusAdminForm, self).__init__(*args, **kwargs)
        #self.fields['nom'].widget.attrs['size']='50'  
        
    class Meta:
        model = Processus
        fields = ('code', 'nom', 'domaine', 'description')
        widgets = {
            'nom': forms.Textarea(attrs={'cols': 125, 'rows':2}),
            'description': forms.Textarea(attrs={'cols': 125, 'rows':8}),
            } 
        
class DomaineAdminForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(DomaineAdminForm, self).__init__(*args, **kwargs)
    
    class Meta:
        model = Domaine
        fields = ('code', 'nom', 'responsable')
        widgets = {
            'nom': forms.Textarea(attrs={'cols': 125, 'rows':2}),
            } 

class CompetenceAdminForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(CompetenceAdminForm, self).__init__(*args, **kwargs)
        
    class Meta:
        model = Competence
        fields = ('__all__')
        widgets = {
            'nom': forms.Textarea(attrs={'cols': 125, 'rows':2}),
            } 
        

class SousCompetenceAdminForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(SousCompetenceAdminForm, self).__init__(*args, **kwargs)
        
    class Meta:
        model = SousCompetence
        fields = ('__all__')
        widgets = {
            'nom': forms.Textarea(attrs={'cols': 125, 'rows':2}),
            } 
        
                
class CompetenceInlineAdminForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(CompetenceInlineAdminForm, self).__init__(*args, **kwargs)
    
    class Meta:
        model = SousCompetence
        fields = ('__all__')
        widgets = {
            'code': forms.Textarea(attrs={'cols': 5, 'rows':1}),
            'nom': forms.Textarea(attrs={'cols': 125, 'rows':2}),
            } 
                
                
class SousCompetenceInlineAdminForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(SousCompetenceInlineAdminForm, self).__init__(*args, **kwargs)
    
    class Meta:
        model = SousCompetence
        fields = ('__all__')
        widgets = {
            'code': forms.Textarea(attrs={'cols': 5, 'rows':1}),
            'nom': forms.Textarea(attrs={'cols': 125, 'rows':1}),
            } 


class ProcessusInlineAdminForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(ProcessusInlineAdminForm, self).__init__(*args, **kwargs)
    
    class Meta:
        model = SousCompetence
        fields = ('__all__')
        widgets = {
            'code': forms.Textarea(attrs={'cols': 5, 'rows':1}),
            'nom': forms.Textarea(attrs={'cols': 75, 'rows':4}),
            'description': forms.Textarea(attrs={'cols': 95, 'rows':6}),
            } 

class ObjectifAdminForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(ObjectifAdminForm, self).__init__(*args, **kwargs)
    
    class Meta:
        model = SousCompetence
        fields = ('__all__')
        widgets = {
            'nom': forms.Textarea(attrs={'cols': 125, 'rows':2}),
            }  


class RessourceAdminForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(RessourceAdminForm, self).__init__(*args, **kwargs)
    
    class Meta:
        model = SousCompetence
        fields = ('__all__')
        widgets = {
            'nom': forms.Textarea(attrs={'cols': 125, 'rows':3}),
            }  

         
class ModuleAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ModuleAdminForm, self).__init__(*args, **kwargs)
        #self.fields['nom'].widget.attrs['size']='50'  
        
    class Meta:
        model = Module
        fields = ('__all__')
        widgets = {
            'nom': forms.Textarea(attrs={'cols': 125, 'rows':2}),
            'description': forms.Textarea(attrs={'cols': 125, 'rows':4}),
            'situation': forms.Textarea(attrs={'cols': 125, 'rows':6}),
            'contenu': forms.Textarea(attrs={'cols': 125, 'rows':4}),
            'didactique': forms.Textarea(attrs={'cols': 125, 'rows':2}),
            'evaluation': forms.Textarea(attrs={'cols': 125, 'rows':2}),
            } 


class UploadAdminForm(forms.ModelForm):
    
    class Meta:
        model = UploadDoc
        fields = ('titre', 'docfile', 'published', )
             