
from django.http.response import HttpResponse
from django.conf import settings

from reportlab.platypus import SimpleDocTemplate

from reportlab.platypus import Paragraph, Spacer, PageBreak, Table, TableStyle, Image
from reportlab.graphics.shapes import Line
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle as PS
style_8_c = PS(name='CORPS', fontName='Helvetica', fontSize=6, alignment = TA_CENTER)
style_normal = PS(name='CORPS', fontName='Helvetica', fontSize=8, alignment = TA_LEFT)
style_bold = PS(name='CORPS', fontName='Helvetica-Bold', fontSize=10, alignment = TA_LEFT)
style_title = PS(name='CORPS', fontName='Helvetica', fontSize=12, alignment = TA_LEFT)
style_adress = PS(name='CORPS', fontName='Helvetica', fontSize=10, alignment = TA_LEFT, leftIndent=300)



class PDFResponse(HttpResponse):
    
    def __init__(self, filename, title='', portrait=True):
        HttpResponse.__init__(self, content_type='application/pdf')
        self['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
        self['Content-Type'] = 'charset=utf-8'
        self.story = []
        image = Image(settings.MEDIA_ROOT + '/media/header.png', width=480, height=80)
        image.hAlign = TA_LEFT
        
        self.story.append(image)
        #self.story.append(Spacer(0,1*cm))
        
        data = [['Filières EDS', title]]
        if portrait:
            t =  Table(data, colWidths=[8*cm,8*cm])
        else:
            t =  Table(data, colWidths=[11*cm,11*cm])
        t.setStyle(TableStyle([ ('ALIGN',(0,0),(0,0),'LEFT'),
                                ('ALIGN',(1,0),(-1,-1),'RIGHT'),
                                ('LINEABOVE', (0,0) ,(-1,-1), 0.5, colors.black),
                                ('LINEBELOW', (0,-1),(-1,-1), 0.5, colors.black),
                            ]))
        t.hAlign = TA_LEFT
        self.story.append(t)
        
        
    
class MyDocTemplate(SimpleDocTemplate):
    
    def __init__(self, name):
        SimpleDocTemplate.__init__(self, name, pagesize=A4, topMargin=0*cm)
        self.fileName = name
        self.PAGE_WIDTH = A4[0]
        self.PAGE_HEIGHT = A4[1]
        self.CENTRE_WIDTH = self.PAGE_WIDTH/2.0
        self.CENTRE_HEIGHT = self.PAGE_HEIGHT/2.0
        
        
    def beforePage(self):
        # page number
        self.canv.saveState()
        self.canv.setFontSize(8)
        self.canv.drawCentredString(self.CENTRE_WIDTH,1*cm,"Page : " + str(self.canv.getPageNumber()))
        self.canv.restoreState()
        
        
    
class MyDocTemplateLandscape(SimpleDocTemplate):
    
    def __init__(self, name):
        SimpleDocTemplate.__init__(self, name, pagesize=landscape(A4), topMargin=0*cm, leftMargin=2*cm)
        self.fileName = name
        self.PAGE_WIDTH = A4[1]
        self.PAGE_HEIGHT = A4[0]
        self.CENTRE_WIDTH = self.PAGE_WIDTH/2.0
        self.CENTRE_HEIGHT = self.PAGE_HEIGHT/2.0
        
    def beforePage(self):
        # page number
        self.canv.saveState()
        self.canv.setFontSize(8)
        self.canv.drawCentredString(self.CENTRE_WIDTH,1*cm,"Page : " + str(self.canv.getPageNumber()))
        self.canv.restoreState()
    
    