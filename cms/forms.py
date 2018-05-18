"""
Created on 17 nov. 2012

@author: alzo
"""
from django import forms
from tinymce.widgets import TinyMCE

from .models import (
    Processus, Module, Domaine, Competence, SousCompetence, Concept, UploadDoc
)


class ConceptAdminForm(forms.ModelForm):
    
    class Meta:
        model = Concept
        fields = ('titre', 'texte', 'published')
        widgets = {
            'texte': TinyMCE(attrs={'cols': 120, 'rows': 30}),
        }
        
  
class ProcessusAdminForm(forms.ModelForm):

    class Meta:
        model = Processus
        fields = ('code', 'nom', 'domaine', 'description')
        widgets = {
            'nom': forms.Textarea(attrs={'cols': 125, 'rows': 2}),
            'description': forms.Textarea(attrs={'cols': 125, 'rows': 8}),
        }

    def __init__(self, *args, **kwargs):
        super(ProcessusAdminForm, self).__init__(*args, **kwargs)


class DomaineAdminForm(forms.ModelForm):

    class Meta:
        model = Domaine
        fields = ('code', 'nom', 'responsable')
        widgets = {
            'nom': forms.Textarea(attrs={'cols': 125, 'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super(DomaineAdminForm, self).__init__(*args, **kwargs)
    

class CompetenceAdminForm(forms.ModelForm):

    class Meta:
        model = Competence
        fields = '__all__'
        widgets = {
            'nom': forms.Textarea(attrs={'cols': 125, 'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super(CompetenceAdminForm, self).__init__(*args, **kwargs)


class SousCompetenceAdminForm(forms.ModelForm):

    class Meta:
        model = SousCompetence
        fields = '__all__'
        widgets = {
            'nom': forms.Textarea(attrs={'cols': 125, 'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super(SousCompetenceAdminForm, self).__init__(*args, **kwargs)


class CompetenceInlineAdminForm(forms.ModelForm):

    class Meta:
        model = SousCompetence
        fields = '__all__'
        widgets = {
            'code': forms.Textarea(attrs={'cols': 5, 'rows': 1}),
            'nom': forms.Textarea(attrs={'cols': 125, 'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super(CompetenceInlineAdminForm, self).__init__(*args, **kwargs)


class SousCompetenceInlineAdminForm(forms.ModelForm):

    class Meta:
        model = SousCompetence
        fields = '__all__'
        widgets = {
            'code': forms.Textarea(attrs={'cols': 5, 'rows': 1}),
            'nom': forms.Textarea(attrs={'cols': 125, 'rows': 1}),
        }

    def __init__(self, *args, **kwargs):
        super(SousCompetenceInlineAdminForm, self).__init__(*args, **kwargs)


class ProcessusInlineAdminForm(forms.ModelForm):

    class Meta:
        model = SousCompetence
        fields = '__all__'
        widgets = {
            'code': forms.Textarea(attrs={'cols': 5, 'rows': 1}),
            'nom': forms.Textarea(attrs={'cols': 75, 'rows': 4}),
            'description': forms.Textarea(attrs={'cols': 95, 'rows': 6}),
        }

    def __init__(self, *args, **kwargs):
        super(ProcessusInlineAdminForm, self).__init__(*args, **kwargs)


class ObjectifAdminForm(forms.ModelForm):

    class Meta:
        model = SousCompetence
        fields = '__all__'
        widgets = {
            'nom': forms.Textarea(attrs={'cols': 125, 'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super(ObjectifAdminForm, self).__init__(*args, **kwargs)


class RessourceAdminForm(forms.ModelForm):

    class Meta:
        model = SousCompetence
        fields = '__all__'
        widgets = {
            'nom': forms.Textarea(attrs={'cols': 125, 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super(RessourceAdminForm, self).__init__(*args, **kwargs)


class ModuleAdminForm(forms.ModelForm):

    class Meta:
        model = Module
        fields = '__all__'
        widgets = {
            'nom': forms.Textarea(attrs={'cols': 50, 'rows': 1}),
            'description': forms.Textarea(attrs={'cols': 125, 'rows': 3}),
            'situation': forms.Textarea(attrs={'cols': 125, 'rows': 4}),
            'contenu': forms.Textarea(attrs={'cols': 125, 'rows': 3}),
            'didactique': forms.Textarea(attrs={'cols': 125, 'rows': 2}),
            'evaluation': forms.Textarea(attrs={'cols': 125, 'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super(ModuleAdminForm, self).__init__(*args, **kwargs)


class UploadAdminForm(forms.ModelForm):
    
    class Meta:
        model = UploadDoc
        fields = ('titre', 'docfile', 'published', )
