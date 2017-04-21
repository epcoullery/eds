from django.contrib import admin

from .models import (Enseignant, Domaine, Competence, SousCompetence, Objectif,
        Ressource, Module, Processus, Document, UploadDoc)

from .forms import (ProcessusAdminForm, ProcessusInlineAdminForm, ModuleAdminForm, DomaineAdminForm, CompetenceAdminForm, 
SousCompetenceInlineAdminForm, CompetenceInlineAdminForm, ObjectifAdminForm, RessourceAdminForm,
SousCompetenceAdminForm, DocumentAdminForm, UploadAdminForm )

# Register your models here.


class SousCompetenceInline(admin.TabularInline):
    form = SousCompetenceInlineAdminForm
    model = SousCompetence
    extra = 0

   
class CompetenceInline(admin.TabularInline):
    form = CompetenceInlineAdminForm
    model = Competence
    extra=0
    #template ='templates/admin/cms/processus/edit_inline/tabular.html'

class SousCompetenceAdmin(admin.ModelAdmin):
    form = SousCompetenceAdminForm
    
    
class RessourceAdmin(admin.ModelAdmin):
    form = RessourceAdminForm
    list_display = ('nom', 'module')
    

class ModuleAdmin(admin.ModelAdmin):
    form = ModuleAdminForm
    inlines = [CompetenceInline,]
    extra = 0
    
    
class ProcessusAdmin(admin.ModelAdmin):   
    form = ProcessusAdminForm


class ObjectifAdmin(admin.ModelAdmin):   
    form = ObjectifAdminForm
    
    
class ProcessusInlineAdmin(admin.TabularInline):
    form = ProcessusInlineAdminForm
    model = Processus
    extra=0
    
    
class CompetenceAdmin(admin.ModelAdmin):
    form = CompetenceAdminForm
    list_display = ('code', 'nom', 'proces_eval')
    list_editable = ('proces_eval',)
    inlines = (SousCompetenceInline,)
    

class DomaineAdmin(admin.ModelAdmin):
    list_display = ('nom', 'responsable',)
    form = DomaineAdminForm
    inlines = [ProcessusInlineAdmin,]


class DocumentAdmin(admin.ModelAdmin):
    form = DocumentAdminForm


class UploadAdmin(admin.ModelAdmin):
    form = UploadAdminForm
    
         
admin.site.register(Enseignant)
admin.site.register(Domaine, DomaineAdmin)
admin.site.register(Competence, CompetenceAdmin)
admin.site.register(SousCompetence, SousCompetenceAdmin)
admin.site.register(Objectif, ObjectifAdmin)
admin.site.register(Ressource, RessourceAdmin)
admin.site.register(Module, ModuleAdmin)
admin.site.register(Processus, ProcessusAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(UploadDoc, UploadAdmin)
