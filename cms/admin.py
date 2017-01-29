from django.contrib import admin
from .models import (Enseignant, Domaine, Competence, SousCompetence, Objectif,
        Ressource, Module, Processus)
from .forms import ProcessusAdminForm, ModuleAdminForm, DomaineAdminForm
# Register your models here.

class SousCompetenceInline(admin.TabularInline):
    model = SousCompetence
    extra = 0
    
class CompetenceInline(admin.TabularInline):
    model = Competence
    extra=0
    #template ='templates/admin/cms/processus/edit_inline/tabular.html'

class RessourceAdmin(admin.ModelAdmin):
    list_display = ('nom', 'module')
    

class ModuleAdmin(admin.ModelAdmin):
    form = ModuleAdminForm
    inlines = [CompetenceInline,]
    extra = 0
    
    
class ProcessusAdmin(admin.ModelAdmin):   
    form = ProcessusAdminForm

class ProcessusAdminInline(admin.TabularInline):
    model = Processus
    extra=0
    
    
class CompetenceAdmin(admin.ModelAdmin):
    list_display = ('code', 'nom', 'module')
    list_editable = ('module',)
    inlines = (SousCompetenceInline,)
    

class DomaineAdmin(admin.ModelAdmin):
    list_display = ('nom', 'responsable',)
    form = DomaineAdminForm
    inlines = [ProcessusAdminInline,]
    
    
admin.site.register(Enseignant)
admin.site.register(Domaine, DomaineAdmin)
admin.site.register(Competence, CompetenceAdmin)
admin.site.register(SousCompetence)
admin.site.register(Objectif)
admin.site.register(Ressource, RessourceAdmin)
admin.site.register(Module, ModuleAdmin)
admin.site.register(Processus, ProcessusAdmin)
