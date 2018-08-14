from django.contrib import admin

from .forms import (
    ProcessusAdminForm, ProcessusInlineAdminForm, ModuleAdminForm,
    DomaineAdminForm, CompetenceAdminForm, SousCompetenceInlineAdminForm,
    CompetenceInlineAdminForm, ObjectifAdminForm, RessourceAdminForm,
    SousCompetenceAdminForm, ConceptAdminForm, UploadAdminForm
)

from .models import (
    Enseignant, Domaine, Competence, SousCompetence, Objectif,
    Ressource, Module, Processus, Concept, UploadDoc
)


class SousCompetenceInline(admin.TabularInline):
    form = SousCompetenceInlineAdminForm
    model = SousCompetence
    extra = 0

   
class CompetenceInline(admin.TabularInline):
    form = CompetenceInlineAdminForm
    model = Competence
    extra = 0


class SousCompetenceAdmin(admin.ModelAdmin):
    form = SousCompetenceAdminForm
    
    
class RessourceAdmin(admin.ModelAdmin):
    form = RessourceAdminForm
    list_display = ('nom', 'module')
    

class ModuleAdmin(admin.ModelAdmin):
    form = ModuleAdminForm
    inlines = [CompetenceInline]
    readonly_fields = ('total_presentiel',)
    extra = 0

    fields = (('code', 'nom'),
              'situation',
              ('contenu', 'contenu_published'),
              ('didactique', 'didactique_published'),
              ('evaluation', 'evaluation_published'),
              ('sem1', 'sem2', 'sem3', 'sem4', 'sem5', 'sem6'),
              ('total_presentiel', 'travail_perso', 'pratique_prof'),
              ('type', ),
              'processus',
              )


class ProcessusAdmin(admin.ModelAdmin):   
    form = ProcessusAdminForm


class ObjectifAdmin(admin.ModelAdmin):   
    form = ObjectifAdminForm
    
    
class ProcessusInlineAdmin(admin.TabularInline):
    form = ProcessusInlineAdminForm
    model = Processus
    extra = 0
    
    
class CompetenceAdmin(admin.ModelAdmin):
    form = CompetenceAdminForm
    list_display = ('code', 'nom', 'proces_eval')
    list_editable = ('proces_eval',)
    inlines = (SousCompetenceInline,)
    

class DomaineAdmin(admin.ModelAdmin):
    list_display = ('nom', 'responsable',)
    form = DomaineAdminForm
    inlines = [ProcessusInlineAdmin]


class ConceptAdmin(admin.ModelAdmin):
    form = ConceptAdminForm


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
admin.site.register(Concept, ConceptAdmin)
admin.site.register(UploadDoc, UploadAdmin)
