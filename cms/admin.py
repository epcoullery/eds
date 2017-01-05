from django.contrib import admin
from .models import (Enseignant, Domaine, Competence, SousCompetence, Objectif,
        Ressource, Module, Processus)
from django.forms.widgets import Widget
from django.forms import widgets
# Register your models here.

class SousCompetenceInline(admin.TabularInline):
    model = SousCompetence
    extra = 0
    
class CompetenceInline(admin.TabularInline):
    model = Competence
    extra=0
    #template ='templates/admin/cms/processus/edit_inline/tabular.html'


class ModuleAdmin(admin.ModelAdmin):
    inlines = [CompetenceInline,]
    extra = 0
    
    
class ProcessusAdmin(admin.ModelAdmin):   
    inlines = (CompetenceInline,) 

class CompetenceAdmin(admin.ModelAdmin):
    inlines = (SousCompetenceInline,)

class RessourceAdmin(admin.ModelAdmin):
    pass


admin.site.register(Enseignant)
admin.site.register(Domaine)
admin.site.register(Competence, CompetenceAdmin)
admin.site.register(SousCompetence)
admin.site.register(Objectif)
admin.site.register(Ressource)
admin.site.register(Module)
admin.site.register(Processus, ProcessusAdmin)
