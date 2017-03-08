# -*- coding: utf-8 -*-
'''
Created on 4 déc. 2012

@author: alzo
'''
import os
from django.shortcuts import render, render_to_response
from django.views.generic import ListView, TemplateView, DetailView
from .models import Domaine, Processus, Module, Document, PDFResponse, MyDocTemplate, MyDocTemplateLandscape
from .models import style_normal, style_bold, style_title
from django.db.models import F, Sum
from django.conf import settings

from django.http import HttpResponseRedirect
from django.http import HttpResponse
from .forms import DocumentForm

from reportlab.pdfgen import canvas

from reportlab.platypus import Paragraph, Spacer, PageBreak, Table, TableStyle, Preformatted
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_LEFT
from reportlab.lib import colors
from reportlab.lib.colors import HexColor

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

   
class HomwPDFView(TemplateView):
    template_name = 'cms/index.html'
    
    def render_to_response(self, context, **response_kwargs):
        
        response = PDFResponse('PlanFormation.pdf' ,'Plan de formation', portrait=False)
        d = Domaine.objects.all().order_by('code')
        p = Processus.objects.all().order_by('code')

        
        data = [['Domaines','Processus', 'Sem1', 'Sem2', 'Sem3','Sem4','Sem5','Sem6'],
                [Preformatted(d[0].__str__(), style_normal, maxLineLength=40), Preformatted(p[0].__str__(), style_normal, maxLineLength=60) , 'M01' , ''    ,''    , ''  , ''  ,''   ],
                [''  , ''    , 'M02' , ''    ,''    , ''  , ''  ,''   ],
                [''  , Preformatted(p[1].__str__(), style_normal, maxLineLength=60) , ''    , '' ,''    , 'M03'  , ''  , ''  ],
                [''  , ''    , ''    , 'M04' ,''    , ''  , ''  , ''  ],
                [Preformatted(d[1].__str__(), style_normal, maxLineLength=40), Preformatted(p[2].__str__(), style_normal, maxLineLength=60) , 'M05' , ''    ,'M06' , ''  , ''  , ''  ],
                [''  , Preformatted(p[3].__str__(), style_normal, maxLineLength=60) , ''    , ''    ,''    , 'M07'  , ''  , 'M09'  ],
                [''  , ''    , ''    , ''    ,''    , 'M08'  , ''  , ''  ],
                [Preformatted(d[2].__str__(), style_normal, maxLineLength=40), Preformatted(p[4].__str__(), style_normal, maxLineLength=60) , ''    , ''    ,''    , 'M10'  , ''  , 'M12'  ],
                [''  , Preformatted(p[5].__str__(), style_normal, maxLineLength=60) , ''    , ''    ,''    , 'M11'  , ''  , ''  ],
                [Preformatted(d[3].__str__(), style_normal, maxLineLength=40), Preformatted(p[6].__str__(), style_normal, maxLineLength=60) , ''    , ''    ,''    , 'M13'  , ''  , 'M14'  ],
                [Preformatted(d[4].__str__(), style_normal, maxLineLength=40), Preformatted(p[7].__str__(), style_normal, maxLineLength=60) , 'M15'    , ''    ,''    , ''  , ''  , ''  ],
                [Preformatted(d[5].__str__(), style_normal, maxLineLength=40), Preformatted(p[8].__str__(), style_normal, maxLineLength=60) , 'M16_1'    , ''    ,'M16_2'    , ''  , 'M16_3'  , ''  ],
                [Preformatted(d[6].__str__(), style_normal, maxLineLength=40), Preformatted(p[9].__str__(), style_normal, maxLineLength=60), 'M17_1'    , ''    ,'M17_2'    , ''  , 'M17_3'  , ''  ],
                [Preformatted(d[7].__str__(), style_normal, maxLineLength=40), Preformatted(p[10].__str__(), style_normal, maxLineLength=60) , 'Macc'    , ''    ,''    , ''  , ''  , ''  ],
            ]
        
        t = Table(data, colWidths=[5.5*cm, 8*cm, 1.5*cm, 1.5*cm,1.5*cm, 1.5*cm,1.5*cm,1.5*cm], spaceBefore=0.5*cm, spaceAfter=1*cm)
        t.setStyle(TableStyle([
            ('SIZE', (0,0), (-1,-1), 8),
            ('FONT', (0,0), (-1,0), 'Helvetica-Bold'),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
            ('ALIGN',(2,0),(-1,-1),'CENTER'),

            #('BOX',(0,0),(-1,-1), 0.25, colors.black),
            ('GRID',(0,0),(-1,-1), 0.25, colors.black),
            ('SPAN',(0,1), (0,4)), #Domaine 1
            ('SPAN',(1,1), (1,2)),
            ('SPAN',(1,3), (1,4)),
            ('SPAN',(0,5), (0,7)), #Domaine 2
            ('SPAN',(1,6), (1,7)),
            ('SPAN',(0,8), (0,9)), #Domaine 3
            ('SPAN',(5,8), (6,8)),
            ('SPAN',(5,9), (6,9)),
            ('SPAN',(2,11), (-1,11)),
            ('SPAN',(2,12), (3,12)),
            ('SPAN',(4,12), (5,12)),
            ('SPAN',(6,12), (7,12)),
            ('SPAN',(2,13), (3,13)),
            ('SPAN',(4,13), (5,13)),
            ('SPAN',(6,13), (7,13)),
            ('SPAN',(2,14), (-1,14)),
            ('BACKGROUND',(0,1), (1,4), colors.orange),
            ('BACKGROUND',(2,1), (2,2), colors.orange),
            ('BACKGROUND',(5,3), (5,3), colors.orange),
            ('BACKGROUND',(3,4), (3,4), colors.orange),
            ('BACKGROUND',(0,5), (1,7), colors.red),
            ('BACKGROUND',(2,5), (2,5), colors.red),
            ('BACKGROUND',(4,5), (4,5), colors.red),
            ('BACKGROUND',(5,6), (5,6), colors.red),
            ('BACKGROperiodesUND',(7,6), (7,6), colors.red),
            ('BACKGROUND',(5,7), (5,7), colors.red),
            ('BACKGROUND',(0,8), (1,9), colors.pink),
            ('BACKGROUND',(5,8), (-1,8), colors.pink),
            ('BACKGROUND',(5,9), (6,9), colors.pink),
            ('BACKGROUND',(0,10), (1,10), HexColor('#AD7FA8')),
            ('BACKGROUND',(5,10), (5,10), HexColor('#AD7FA8')),
            ('BACKGROUND',(7,10), (7,10), HexColor('#AD7FA8')),
            ('BACKGROUND',(0,11), (-1,11), HexColor('#729FCF')),
            ('BACKGROUND',(0,12), (-1,12), colors.lightgreen),
            ('BACKGROUND',(0,13), (-1,13), colors.white),
            ('BACKGROUND',(0,14), (-1,14), colors.lightgrey),
        ]))

        t.hAlign = 0
        response.story.append(t)
        
        doc = MyDocTemplateLandscape(response)  
        doc.build(response.story)
        
        return response
    
    
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

def Preformatted_left(text):
    return Preformatted(text, style_normal, maxLineLength=15)


def Preformatted_right(text):
    return Preformatted(text, style_normal, maxLineLength=110)


class ModulePDF(DetailView):

    template_name = 'cms/module_detail.html'
    model = Module
    
    def get_object(self):
        # Call the superclass
        return super(ModulePDF, self).get_object()

            
            
    def render_to_response(self, context, **response_kwargs):
        #return DetailView.render_to_response(self, context, **response_kwargs)    
        m = self.get_object()
        response = PDFResponse('Module_{0}.pdf'.format(m.code) ,'Module de formation')
       
        
        str_comp = ''
        for c in m.competence_set.all():
            str_comp += '- {0} ({1})\n'.format(c.nom, c.code)
            if self.request.user.is_authenticated:
                for sc in c.souscompetence_set.all():
                    str_comp += '    -- {0}\n'.format(sc.nom)
                    
        str_res = ''
        for c in m.ressource_set.all():
            str_res += '- {0}\n'.format(c.nom)
            
        str_obj = ''
        for c in m.objectif_set.all():
            str_obj += '- {0}\n'.format(c.nom)
            
        lines = m.contenu.split('\n')
        str_con = ''
        for l in lines:
            str_con += '{0}\n'.format(l)
        
        response.story.append(Spacer(0,1*cm))
        response.story.append(Paragraph(m.__str__(), style_title))   
         
        data = [[Preformatted_left('Domaine'), Preformatted_right(m.processus.domaine.__str__())],
                [Preformatted_left('Processus'), Preformatted_right(m.processus.__str__())],
                [Preformatted_left('Situation emblématique'), Preformatted_right(m.situation)],
                [Preformatted_left('Compétences visées'), Preformatted_right(str_comp)],
                [Preformatted_left('Ressources à acquérir'), Preformatted_right(str_res)],
                [Preformatted_left('Objectifs à atteindre'), Preformatted_right(str_obj)],
                [Preformatted_left('Contenu'), Preformatted_right(str_con)],
                [Preformatted_left('Evaluation'), Preformatted_right(m.evaluation)],
                [Preformatted_left('Type'), Preformatted_right('{0}, obligatoire'.format(m.type))],
                [Preformatted_left('Semestre'), Preformatted_right('Sem. {0}'.format(m.semestre))],
                [Preformatted_left('Présentiel'), Preformatted_right('{0} heures'.format(m.periode_presentiel))],
                [Preformatted_left('Travail personnel'), Preformatted_right('{0} heures'.format(m.travail_perso))],
                [Preformatted_left('Responsable'), Preformatted_right(m.processus.domaine.responsable.descr())],
            ]
        t =  Table(data, colWidths=[2.5*cm,10*cm])
        t.setStyle(TableStyle([ ('ALIGN',(0,0),(-1,-1),'LEFT'),
                                ('VALIGN',(0,0),(-1,-1),'TOP'),
                                ('LEFTPADDING', (0,0),(-1,-1), 0),
                            ]))
        t.hAlign=0
        response.story.append(Spacer(0,1*cm))
        response.story.append(t)
        
        
        doc = MyDocTemplate(response)  
        doc.build(response.story)
        
        return response

"""
Calcul du nombre de périodes de formation
"""    
def get_context(context):
    liste = Module.objects.exclude(periode_presentiel = 0)
    #context['tot'] = liste.aggregate(Sum(F('periode_presentiel')))

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
    context['tot'] = context['tot1']['sem1__sum'] + context['tot2']['sem2__sum'] + context['tot3']['sem3__sum'] + \
                    context['tot4']['sem4__sum'] + context['tot5']['sem5__sum'] + context['tot6']['sem6__sum'] 
    
    return context
    
    
class PeriodeView(TemplateView):
    template_name = 'cms/periodes.html'
    
    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)
        return get_context(context)   

  
class PeriodePDFView(TemplateView):  
    template_name = 'cms/periodes.html'
    
    def render_to_response(self, context, **response_kwargs):
        
        response = PDFResponse('Périodes.pdf' ,'Périodes de formation')
        context = get_context(context)
        
        data = [['Semestre 1', '{0} h.'.format(context['tot1']['sem1__sum']),'', 'Semestre 2', '{0} h.'.format(context['tot2']['sem2__sum'])],               
                [context['sem1'][0], '{0} h.'.format(context['sem1'][0].sem1),'', context['sem2'][0], '{0} h.'.format(context['sem2'][0].sem2) ],
                [context['sem1'][1], '{0} h.'.format(context['sem1'][1].sem1),'', context['sem2'][1], '{0} h.'.format(context['sem2'][1].sem2) ],
                [context['sem1'][2], '{0} h.'.format(context['sem1'][2].sem1),'', context['sem2'][2], '{0} h.'.format(context['sem2'][2].sem2) ],
                [context['sem1'][3], '{0} h.'.format(context['sem1'][3].sem1),'', context['sem2'][3], '{0} h.'.format(context['sem2'][3].sem2) ],
                [context['sem1'][4], '{0} h.'.format(context['sem1'][4].sem1),'', '', ''],
                [context['sem1'][5], '{0} h.'.format(context['sem1'][5].sem1),'', '', ''],
                
                
                ['Semestre 3', '{0} h.'.format(context['tot3']['sem3__sum']),'', 'Semestre 4', '{0} h.'.format(context['tot4']['sem4__sum'])],
                [context['sem3'][0], '{0} h.'.format(context['sem3'][0].sem3),'', context['sem4'][0], '{0} h.'.format(context['sem4'][0].sem4) ],
                [context['sem3'][1], '{0} h.'.format(context['sem3'][1].sem3),'', context['sem4'][1], '{0} h.'.format(context['sem4'][1].sem4) ],
                [context['sem3'][2], '{0} h.'.format(context['sem3'][2].sem3),'', context['sem4'][2], '{0} h.'.format(context['sem4'][2].sem4) ],
                [context['sem3'][3], '{0} h.'.format(context['sem3'][3].sem3),'', context['sem4'][3], '{0} h.'.format(context['sem4'][3].sem4) ],
                [context['sem3'][4], '{0} h.'.format(context['sem3'][4].sem3),'', context['sem4'][4], '{0} h.'.format(context['sem4'][4].sem4) ],
                [context['sem3'][5], '{0} h.'.format(context['sem3'][5].sem3),'', context['sem4'][5], '{0} h.'.format(context['sem4'][5].sem4) ],
                
                ['Semestre 5', '{0} h.'.format(context['tot5']['sem5__sum']),'', 'Semestre 6', '{0} h.'.format(context['tot6']['sem6__sum'])],
                [context['sem5'][0], '{0} h.'.format(context['sem5'][0].sem5),'', context['sem6'][0], '{0} h.'.format(context['sem6'][0].sem6) ],
                [context['sem5'][1], '{0} h.'.format(context['sem5'][1].sem5),'', context['sem6'][1], '{0} h.'.format(context['sem6'][1].sem6) ],
                [context['sem5'][2], '{0} h.'.format(context['sem5'][2].sem5),'', context['sem6'][2], '{0} h.'.format(context['sem6'][2].sem6) ],
                [context['sem5'][3], '{0} h.'.format(context['sem5'][3].sem5),'', context['sem6'][3], '{0} h.'.format(context['sem6'][3].sem6) ],
                [context['sem5'][4], '{0} h.'.format(context['sem5'][4].sem5),'', '', '' ],
                [context['sem5'][5], '{0} h.'.format(context['sem5'][5].sem5),'', '', '' ],
                 ]
        
        t = Table(data, colWidths=[6.5*cm,1*cm, 1*cm, 6.5*cm, 1*cm], spaceBefore=2*cm, spaceAfter=1.5*cm)
        t.setStyle(TableStyle([ ('ALIGN',(0,0),(-1,-1),'LEFT'),
                                ('VALIGN',(0,0),(-1,-1),'TOP'),
                                ('LEFTPADDING', (0,0),(-1,-1), 0),
                                ('SIZE', (0,0), (-1,-1), 8),
                                ('ALIGN', (1,0), (1,-1), 'RIGHT'),
                                ('ALIGN', (-1,0), (-1,-1), 'RIGHT'),
                                ('LINEBELOW', (0,0), (1,0), 1, colors.black),
                                ('LINEBELOW', (3,0), (-1,0), 1, colors.black),
                               
                                ('TOPPADDING', (0,7), (-1,7), 15),
                                ('LINEBELOW', (0,7), (1,7), 1, colors.black),
                                ('LINEBELOW', (3,7), (-1,7), 1, colors.black),
                                ('TOPPADDING', (0,14), (-1,14), 15),
                                ('LINEBELOW', (0,14), (1,14), 1, colors.black),
                                ('LINEBELOW', (3,14), (-1,14), 1, colors.black),
                                ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                ('FONT', (0, 7), (-1, 7), 'Helvetica-Bold'),
                                ('FONT', (0, 14), (-1, 14), 'Helvetica-Bold'),
                            ]))
        
        t.hAlign = 0
        response.story.append(t)
        
        response.story.append(Paragraph('Total des heures de cours: {0} heures'.format(context['tot']), style_normal))
        doc = MyDocTemplate(response)  
        doc.build(response.story)
        
        return response


class AddDocument(TemplateView):
    template_name = 'cms/upload.html'
    
    def post(self, request):
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()
        
        return HttpResponseRedirect('')
    
    def get(self, request):
        form = DocumentForm()
        return render (request, 'cms/upload.html', {'form': form})




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
    

def pdf_view(request):
    with open('/home/alzo/dev/eds/media/media/EDS_Calendrier_2017.pdf', 'r') as pdf:
        response = HttpResponse(pdf.read().decode('latin-1') , content_type='application/pdf')
        response['Content-Disposition'] = 'inline;filename=some_file.pdf'
        return response
    pdf.closed  
    
    
def import_xls_file(request):
    import xlrd
    
    if request.method == 'POST':
        xlspath = '/home/alzo/Export_CLOEE_FE.xls'
        with xlrd.open_workbook(xlspath) as book:
            sheet = book.sheet_by_index(0)
            print(sheet.ncols)
            print(sheet.nrows)
        
        
    if request.method == 'GET':
        xlspath = '/home/alzo/Export_CLOEE_FE.xls'
        with xlrd.open_workbook(xlspath) as book:
            sheet = book.sheet_by_index(0)
            for rownum in range(1,sheet.nrows): 
                print(int(sheet.row_values(rownum)[0]))
                

