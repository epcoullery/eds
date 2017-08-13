
from django.http.response import HttpResponse
from django.conf import settings

from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Frame
from reportlab.platypus import Table, TableStyle, Image
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle as PS


style_8_c = PS(name='CORPS', fontName='Helvetica', fontSize=6, alignment=TA_CENTER)
style_normal = PS(name='CORPS', fontName='Helvetica', fontSize=8, alignment=TA_LEFT)
style_bold = PS(name='CORPS', fontName='Helvetica-Bold', fontSize=10, alignment=TA_LEFT)
style_title = PS(name='CORPS', fontName='Helvetica', fontSize=12, alignment=TA_LEFT)
style_adress = PS(name='CORPS', fontName='Helvetica', fontSize=10, alignment=TA_LEFT, leftIndent=300)


class PDFResponse(HttpResponse):
    
    def __init__(self, filename, title='', portrait=True):
        HttpResponse.__init__(self, content_type='application/pdf')
        self['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
        self['Content-Type'] = 'charset=utf-8'
        self.story = []
        image = Image(settings.MEDIA_ROOT + '/media/header.png', width=400, height=80)
        image.hAlign = TA_LEFT
        
        self.story.append(image)
        data = [['Filières EDS', title]]
        if portrait:
            t = Table(data, colWidths=[8*cm, 8*cm])
        else:
            t = Table(data, colWidths=[11*cm, 11*cm])
        t.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
            ('LINEABOVE', (0, 0), (-1, -1), 0.5, colors.black),
            ('LINEBELOW', (0, -1), (-1, -1), 0.5, colors.black),
        ]))
        t.hAlign = TA_LEFT
        self.story.append(t)
        

class MyDocTemplate(SimpleDocTemplate):
    
    def __init__(self, name):
        SimpleDocTemplate.__init__(self, name, pagesize=A4, topMargin=0.5*cm, leftMargin=1*cm)
        self.fileName = name
        self.PAGE_WIDTH = A4[0]
        self.PAGE_HEIGHT = A4[1]
        self.CENTRE_WIDTH = self.PAGE_WIDTH/2.0
        self.CENTRE_HEIGHT = self.PAGE_HEIGHT/2.0
        
    def beforePage(self):
        # page number
        self.canv.saveState()
        self.canv.setFontSize(8)
        self.canv.drawCentredString(self.CENTRE_WIDTH, 1*cm, "Page : " + str(self.canv.getPageNumber()))
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
        self.canv.drawCentredString(self.CENTRE_WIDTH, 1*cm, "Page : " + str(self.canv.getPageNumber()))
        self.canv.restoreState()


class PeriodPDF(object):
    """Imprime les heures de cours par semestre"""
    def __init__(self, filename):
        self.canv = canvas.Canvas(filename, pagesize=A4)
        self.canv.setPageCompression(0)
        self.canv.setFont('Helvetica', 9)
        header_frame = Frame(1.2*cm, 24*cm, 18*cm, 5*cm, showBoundary=0)
        story = []
        image = Image(settings.MEDIA_ROOT + 'logo.png', width=520, height=90)
        story.append(image)
        data = [['Filières EDS', 'Périodes de formation']]
        t = Table(data, colWidths=[8.5*cm, 8.5*cm], spaceBefore=0, spaceAfter=0, hAlign=TA_LEFT)
        t.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
            ('LINEABOVE', (0, 0), (-1, -1), 0.5, colors.black),
            ('LINEBELOW', (0, -1), (-1, -1), 0.5, colors.black),
        ]))
        story.append(t)
        header_frame.addFromList(story, self.canv)

    def produce_half_year(self, half_year_id, modules, total):
        initial_pos_x = [2, 11]
        initial_pos_y = [17, 17, 10, 10, 3, 3]
        width = 7*cm
        height = 6.5*cm

        x = initial_pos_x[(half_year_id-1) % 2]*cm
        y = initial_pos_y[half_year_id-1]*cm

        my_frame = Frame(x, y, width, height, showBoundary=0)
        data = [['Semestre {0}'.format(half_year_id), '{0} h.'.format(total)]]
        for line in modules:
            value = getattr(line, 'sem{0}'.format(half_year_id))
            data.append([line.nom, '{0} h.'.format(value)])

        t = Table(data, colWidths=[7*cm, 1*cm], spaceBefore=0, spaceAfter=0, hAlign=TA_LEFT)
        t.setStyle(TableStyle([('ALIGN', (0, 0), (0, 0), 'LEFT'),
                               ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
                               ('LINEBELOW', (0, 0), (1, 0), 1, colors.black),
                               ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'), ]))
        story = [t]
        my_frame.addFromList(story, self.canv)

    def print_total(self, total):
        self.canv.drawString(2*cm, 2*cm, 'Total de la formation: {0} heures'.format(total))
