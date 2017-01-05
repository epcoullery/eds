# -*- encoding: utf-8 -*-
'''
Created on 17 nov. 2012

@author: alzo
'''

from django import forms

class DocumentForm(forms.Form):
    docfile = forms.FileField(label='Selectionner un fichier',
                          help_text='Taille max.: 42 megabytes')   