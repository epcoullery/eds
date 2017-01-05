# -*- coding: utf-8 -*-
'''
Created on 4 déc. 2012

@author: alzo
'''
import os
from django.shortcuts import render
from django.views.generic import ListView, TemplateView, DetailView
from .models import Domaine, Processus, Module, Document, Document
from django.db.models import F, Sum
from django.conf import settings

from django.http import HttpResponseRedirect
from django.http import HttpResponse
from .forms import DocumentForm

# Create your views here.

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


    
    
class PeriodeView(TemplateView):
    template_name = 'cms/periodes.html'
    
    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)
        liste = Module.objects.exclude(periode_presentiel = 0)
        context['tot'] = liste.aggregate(Sum(F('periode_presentiel')))
        context['sem1'] = liste.exclude(sem1 = 0)
        context['tot1'] = liste.aggregate(Sum(F('sem1')))
        context['sem2'] = liste.exclude(sem2 = 0)
        context['tot2'] = liste.aggregate(Sum(F('sem2')))
        context['sem3'] = liste.exclude(sem3 = 0)
        context['tot3'] = liste.aggregate(Sum(F('sem3')))
        context['sem4'] = liste.exclude(sem4 = 0)
        context['tot4'] = liste.aggregate(Sum(F('sem4')))
        context['sem5'] = liste.exclude(sem5 = 0)
        context['tot5'] = liste.aggregate(Sum(F('sem5')))
        context['sem6'] = liste.exclude(sem6 = 0)
        context['tot6'] = liste.aggregate(Sum(F('sem6')))
        
        return context   
    
    


def AddDoc(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()
            return HttpResponseRedirect('')
    else:
        form = DocumentForm()

    documents = Document.objects.all()
    return render (request, 'cms/upload.html', {'documents': documents,'form': form})


def Download(request, file_name):
    f = os.path.join(settings.MEDIA_ROOT, file_name)
    response = HttpResponse(content_type='application/pdf')   
    response['Content-Disposition'] = 'attachment; filename={0}'.format(file_name)
    response['Content-Length'] = os.stat(f).st_size
    return response
    
       
    