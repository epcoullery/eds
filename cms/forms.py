# -*- encoding: utf-8 -*-
'''
Created on 17 nov. 2012

@author: alzo
'''
from .models import Processus, Module, Domaine
from django import forms

from django.contrib import admin
from _collections_abc import __all__
#from django.forms import Textarea, TextInput


class DocumentForm(forms.Form):
    docfile = forms.FileField(label='Selectionner un fichier', help_text='Taille max.: 42 megabytes')
    
class ProcessusAdminForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(ProcessusAdminForm, self).__init__(*args, **kwargs)
        #self.fields['nom'].widget.attrs['size']='50'  
        
    class Meta:
        model = Processus
        fields = ('code', 'nom', 'domaine', 'description')
        widgets = {
            'nom': forms.Textarea(attrs={'cols': 75, 'rows':2}),
            } 
        
class DomaineAdminForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(DomaineAdminForm, self).__init__(*args, **kwargs)
    
    class Meta:
        model = Domaine
        fields = ('code', 'nom', 'responsable')
        widgets = {
            'nom': forms.Textarea(attrs={'cols': 75, 'rows':2}),
            } 
       
class ModuleAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ModuleAdminForm, self).__init__(*args, **kwargs)
        #self.fields['nom'].widget.attrs['size']='50'  
        
    class Meta:
        model = Module
        fields = ('__all__')
        widgets = {
            'nom': forms.Textarea(attrs={'cols': 73, 'rows':2}),
            'description': forms.Textarea(attrs={'cols': 73, 'rows':4}),
            'situation': forms.Textarea(attrs={'cols': 73, 'rows':6}),
            'contenu': forms.Textarea(attrs={'cols': 73, 'rows':4}),
            'didactique': forms.Textarea(attrs={'cols': 73, 'rows':4}),
            'evaluation': forms.Textarea(attrs={'cols': 73, 'rows':2}),
            } 
        