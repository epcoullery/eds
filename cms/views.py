"""
Created on 4 déc. 2012

@author: alzo
"""
import os
import tempfile


from django.db.models import Sum
from django.http import HttpResponse
from django.views.generic import ListView, TemplateView, DetailView

from cms.pdf import PeriodeSemestrePdf, ModuleDescriptionPdf, FormationPlanPdf

from cms.models import (
    Domaine, Processus, Module, Competence, Concept, UploadDoc
)


class HomeView(TemplateView):
    template_name = 'cms/index.html'
    
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        for d in Domaine.objects.all().order_by('code'):
            context[d.code] = d
        for c in Processus.objects.all().order_by('code'):
            context[c.code] = c
        for m in Module.objects.all().order_by('code'):
            context[m.code] = m
        return context

    
class DomaineDetailView(DetailView): 
    template_name = 'cms/domaine_detail.html'
    model = Domaine 
    

class DomaineListView(ListView): 
    template_name = 'cms/domaine_list.html'
    model = Domaine 
    
    
class ProcessusDetailView(DetailView): 
    template_name = 'cms/processus_detail.html'
    model = Processus
    

class ProcessusListView(ListView): 
    template_name = 'cms/processus_list.html'
    model = Processus 
    
    
class ModuleDetailView(DetailView): 
    template_name = 'cms/module_detail.html'
    model = Module


class ModuleListView(ListView):
    template_name = 'cms/module_list.html'
    model = Module


class EvaluationView(ListView):
    template_name = 'cms/evaluation.html'
    model = Processus


class ConceptDetailView(DetailView):
    template_name = 'cms/concept_detail.html'
    model = Concept


class UploadDocListView(ListView):
    template_name = 'cms/uploaddoc_list.html'
    model = UploadDoc

    def get_queryset(self, **kwargs):
        query = UploadDoc.objects.filter(published=True)
        return query


class UploadDocDetailView(DetailView):
    """
    Display uploaded docs
    """
    template_name = 'cms/uploaddoc_detail.html'
    model = UploadDoc


def print_module_pdf(request, pk):
    filename = 'module.pdf'
    path = os.path.join(tempfile.gettempdir(), filename)
    pdf = ModuleDescriptionPdf(path)
    module = Module.objects.get(pk=pk)
    pdf.produce(module)

    with open(path, mode='rb') as fh:
        response = HttpResponse(fh.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="EDS_module_{0}.pdf"'.format(module.code)
    return response


def print_plan_formation(request):
    filename = 'plan_formation.pdf'
    path = os.path.join(tempfile.gettempdir(), filename)
    pdf = FormationPlanPdf(path)
    domain = Domaine.objects.all().order_by('code')
    process = Processus.objects.all().order_by('code')
    pdf.produce(domain, process)

    with open(path, mode='rb') as fh:
        response = HttpResponse(fh.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="EDS_plan_formation.pdf"'
    return response


def print_periode_formation(request):
    filename = 'periode_formation.pdf'
    path = os.path.join(tempfile.gettempdir(), filename)
    context = {}
    context = get_detail_semestre(context)
    pdf = PeriodeSemestrePdf(path)
    pdf.produce(context)

    with open(path, mode='rb') as fh:
        response = HttpResponse(fh.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="{0}"'.format(filename)
    return response


def get_detail_semestre(context):
    """
    Retrive periods
    """
    context['tot']= 0
    liste = Module.objects.filter(pratique_prof=0)
    for i in range(1, 7):
        sss = 'sem{}'.format(i)
        tot_sem = liste.aggregate(Sum(sss))['{}__sum'.format(sss)]  # total du semestre
        context.update({
            'tot{}'.format(i): tot_sem
        })
        context['tot'] += tot_sem  # total des semestres

    context['modules'] = liste
    return context
    
    
class PeriodeView(TemplateView):
    template_name = 'cms/periodes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return get_detail_semestre(context)


class CompetenceListView(ListView):
    model = Competence
    template_name = 'cms/competence_list.html'


class TravailPersoListView(ListView):
    model = Module
    template_name = 'cms/travail_perso.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_detail_semestre(context)
        context.update({
            'total_perso' :  Module.objects.aggregate((Sum('travail_perso')))['travail_perso__sum'],
            'total_presentiel' : context['tot'],
            'total_pratique': Module.objects.aggregate((Sum('pratique_prof')))['pratique_prof__sum']
        })
        return context
