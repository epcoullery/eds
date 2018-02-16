"""
Created on 4 déc. 2012

@author: alzo
"""
import os
import tempfile

from django.views.generic import ListView, TemplateView, DetailView
from django.db.models import F, Sum
from django.http import HttpResponse

from cms.pdf import PeriodSemesterPdf, ModuleDescriptionPdf, FormationPlanPdf
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
    context = get_context(context)
    pdf = PeriodSemesterPdf(path)
    pdf.produce(context)

    with open(path, mode='rb') as fh:
        response = HttpResponse(fh.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="{0}"'.format(filename)
    return response


def get_context(context):
    """
    Retrive periods
    """
    # liste = Module.objects.exclude(total_presentiel=0)
    liste = Module.objects.filter(pratique_prof=0)
    context['sem1'] = liste.exclude(sem1=0)
    context['tot1'] = liste.aggregate(Sum(F('sem1')))['sem1__sum']
    context['sem2'] = liste.exclude(sem2=0)
    context['tot2'] = liste.aggregate(Sum(F('sem2')))['sem2__sum']
    context['sem3'] = liste.exclude(sem3=0)
    context['tot3'] = liste.aggregate(Sum(F('sem3')))['sem3__sum']
    context['sem4'] = liste.exclude(sem4=0)
    context['tot4'] = liste.aggregate(Sum(F('sem4')))['sem4__sum']
    context['sem5'] = liste.exclude(sem5=0)
    context['tot5'] = liste.aggregate(Sum(F('sem5')))['sem5__sum']
    context['sem6'] = liste.exclude(sem6=0)
    context['tot6'] = liste.aggregate(Sum(F('sem6')))['sem6__sum']

    context['tot'] = (
        context['tot1'] + context['tot2'] + context['tot3'] + context['tot4']
        + context['tot5'] + context['tot6']
    )
    return context
    
    
class PeriodeView(TemplateView):
    template_name = 'cms/periodes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return get_context(context)


class CompetenceListView(ListView):
    model = Competence
    template_name = 'cms/competence_list.html'


class TravailPersoListView(ListView):
    model = Module
    template_name = 'cms/travail_perso.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_context(context)
        context['total_perso'] = Module.objects.aggregate((Sum('travail_perso')))['travail_perso__sum']
        context['total_presentiel'] = context['tot']
        context['total_pratique'] = Module.objects.aggregate((Sum('pratique_prof')))['pratique_prof__sum']
        return get_context(context)   
