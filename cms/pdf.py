
from django.http.response import HttpResponse
from django.conf import settings
from collections import OrderedDict
from reportlab.platypus import (SimpleDocTemplate, Spacer, Frame, Paragraph, Preformatted,
                                BaseDocTemplate, PageTemplate, NextPageTemplate)
from reportlab.platypus import Table, TableStyle, Image
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle as ps
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib.styles import getSampleStyleSheet

style_8_c = ps(name='CORPS', fontName='Helvetica', fontSize=6, alignment=TA_CENTER)
style_normal = ps(name='CORPS', fontName='Helvetica', fontSize=9, alignment=TA_LEFT)
style_bold = ps(name='CORPS', fontName='Helvetica-Bold', fontSize=10, alignment=TA_LEFT, leftIndent=0.3*cm)
style_title = ps(name='CORPS', fontName='Helvetica', fontSize=12, alignment=TA_LEFT)
style_adress = ps(name='CORPS', fontName='Helvetica', fontSize=10, alignment=TA_LEFT, leftIndent=300)


class MyESDocTemplate(BaseDocTemplate):

    def __init__(self, filename, titles=['',''], pageSize=A4):
        super().__init__(filename, pagesize=pageSize, _pageBreakQuick=0)

        self.bottomMargin = 1*cm
        self.letfMargin = 1.5*cm
        self.titles = titles
        self.page_width = (self.width + self.leftMargin * 2)
        self.page_height = (self.height + self.bottomMargin * 2)

        styles = getSampleStyleSheet()

        # Setting up the frames, frames are use for dynamic content not fixed page elements
        first_page_table_frame = Frame(self.leftMargin, self.bottomMargin, self.width+1*cm, self.height - 2*cm,
                                       id='small_table', showBoundary=0)
        later_pages_table_frame = Frame(self.leftMargin, self.bottomMargin, self.width+1*cm, self.height, id='large_table', showBoundary=0)

        # Creating the page templates
        first_page = PageTemplate(id='FirstPage', frames=[first_page_table_frame], onPage=self.on_first_page)
        later_pages = PageTemplate(id='LaterPages', frames=[later_pages_table_frame], onPage=self.add_default_info)
        self.addPageTemplates([first_page, later_pages])
        # Tell Reportlab to use the other template on the later pages,
        # by the default the first template that was added is used for the first page.
        self.flowable =[NextPageTemplate(['*', 'LaterPages'])]


    def on_first_page(self, canvas, doc):
        canvas.saveState()
        canvas.drawImage(settings.MEDIA_ROOT + 'logo_EPC.png', self.leftMargin, self.height - 1*cm, 5 * cm, 5 * cm,
                         preserveAspectRatio=True)
        canvas.drawImage(settings.MEDIA_ROOT + 'logo_ESNE.png', self.width-2*cm, self.height - 1*cm, 5 * cm, 5 * cm,
                         preserveAspectRatio=True)
        self._draw_title(canvas, self.page_height - 1.5 * cm)
        # self.add_default_info(canvas, doc)
        canvas.restoreState()

    def add_default_info(self, canvas, doc):
        canvas.saveState()
        self._draw_title(canvas, self.page_height+1*cm)
        canvas.restoreState()

    def _draw_title(self, canvas, height):
        width = self.leftMargin + self.width
        x = self.leftMargin
        y = height
        canvas.line(x, y, width, y)
        y -= 15
        canvas.drawString(x, y, self.titles[0])
        canvas.drawRightString(width, y, self.titles[1])
        y -= 8
        canvas.line(x, y, width, y)



class MyDocTemplateES(SimpleDocTemplate):
    def __init__(self, filename, title_left, title_right, portrait=True):
        if portrait is True:
            page_size = A4
            column_width = 8 * cm
            my_frame = Frame(2*cm, 24*cm, 17*cm, 5*cm, showBoundary=1)
        else:
            page_size = landscape(A4)
            my_frame = Frame(2*cm, 16*cm, 25*cm, 5*cm, showBoundary=1)
            column_width = 13 * cm
        self.flowable = list()
        SimpleDocTemplate.__init__(self, filename, pagesize=page_size,
                                   topMargin=0 * cm,
                                   leftMargin=2 * cm,
                                   rightMargin=2 * cm,
                                   bottomMargin=0.5 * cm,
                                   )

        self.fileName = filename
        width, height = page_size
        self.textWidth = width - 2*cm
        self.canv = canvas.Canvas(filename, pagesize=page_size)
        self.canv.drawImage(settings.MEDIA_ROOT + 'logo_EPC.png', 2 * cm, 17* cm, 5 * cm, 5 * cm,
                            preserveAspectRatio=True)
        self.canv.drawImage(settings.MEDIA_ROOT + 'logo_ESNE.png', 14 * cm, 25.5 * cm, 5 * cm, 5 * cm,
                            preserveAspectRatio=True)

        string_width = stringWidth(title_right, 'Helvetica-Bold', 12)
        self.canv.setFont('Helvetica-Bold', 12)
        self.canv.line(2 * cm, 25.5 * cm, 19 * cm, 25.5 * cm)
        self.canv.drawString(2 * cm, 25 * cm, title_left)
        self.canv.drawString(self.textWidth-string_width, 25*cm, title_right)
        self.canv.line(2 * cm, 24.6 * cm, 19 * cm, 24.6 * cm)
        self.canv.setFont('Helvetica', 10)

        my_frame.addFromList(self.flowable, self.canv)

        """
        self.fileName = filename
        self.canv = canvas.Canvas(filename, pagesize=A4)
        im1 = Image(settings.MEDIA_ROOT + 'logo_EPC.png', width=170, height=80)
        im2 = Image(settings.MEDIA_ROOT + 'logo_ESNE.png', width=170, height=80)
        data = list()
        data.append([im1, im2])
        data.append([Spacer(0, 0.5 * cm)])
        data.append([title_left, title_right])
        t = Table(data, colWidths=[column_width] * 2, hAlign=TA_LEFT)
        t.setStyle(
            TableStyle(
                [
                    ('SIZE', (0, 0), (-1, -1), 9),
                    ('FONT', (0, 0), (-1, -1), 'Helvetica-Bold'),
                    ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                    ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
                    ('LINEABOVE', (0, 2), (-1, 2), 0.5, colors.black),
                    ('LINEBELOW', (0, -1), (-1, -1), 0.5, colors.black),
                ]
            )
        )
        self.flowable.append(t)
        """


    def beforePage(self):
        # page number
        self.canv.saveState()
        self.canv.setFontSize(8)
        self.canv.drawCentredString(self.pagesize[0] / 2, 0.5 * cm, "Page : " + str(self.canv.getPageNumber()))
        self.canv.restoreState()


class ModulePdf(MyESDocTemplate):

    def __init__(self, filename):
        super().__init__(filename, ['Formation EDS', 'Module de formation'])

    def preformatted_left(self, txt):
        return Preformatted(txt, style_normal, maxLineLength=15)

    def preformatted_right(self, txt):
        return Preformatted(txt, style_normal, maxLineLength=97)

    def produce(self, module):
        str_comp = ''
        for c in module.competence_set.all():
            str_comp += '- {0} ({1})\n'.format(c.nom, c.code)
            """
            if self.request.user.is_authenticated:

                for sc in c.souscompetence_set.all():
                    str_comp += '    -- {0}\n'.format(sc.nom)
            """

        str_scom = ''
        for c in module.competence_set.all():
            for sc in c.souscompetence_set.all():
                str_scom += '- {0} (voir {1})\n'.format(sc.nom, c.code)

        str_res = ''
        for c in module.ressource_set.all():
            str_res += '- {0}\n'.format(c.nom)

        str_obj = ''
        for c in module.objectif_set.all():
            str_obj += '- {0}\n'.format(c.nom)

        lines = module.contenu.split('\n')
        str_con = ''
        for l in lines:
            str_con += '{0}\n'.format(l)

        lines = module.evaluation.split('\n')
        str_con = ''
        for l in lines:
            str_con += '{0}\n'.format(l)

        # self.flowable.append(Spacer(0, 0.5 * cm))
        self.flowable.append(Paragraph(module.__str__(), style_bold, ))
        self.flowable.append(Spacer(0, 0.5 * cm))

        data = [
            [self.preformatted_left('Domaine'), self.preformatted_right(module.processus.domaine.__str__())],
            [self.preformatted_left('Processus'), self.preformatted_right(module.processus.__str__())],
            [self.preformatted_left('Situation emblématique'), self.preformatted_right(module.situation)],
            [self.preformatted_left('Compétences visées'), self.preformatted_right(str_comp)],
            [self.preformatted_left('Plus-value sur le CFC ASE'), self.preformatted_right(str_scom)],
            # [Preformatted_left('Ressources à acquérir'), Preformatted_right(str_res)],
            [self.preformatted_left('Objectifs à atteindre'), self.preformatted_right(str_obj)],
            [self.preformatted_left('Didactique'), self.preformatted_right(module.didactique)],
            # [Preformatted_left('Contenu'), Preformatted_right(str_con)],
            [self.preformatted_left('Evaluation'), self.preformatted_right(module.evaluation)],
            [self.preformatted_left('Type'), self.preformatted_right('{0}, obligatoire'.format(module.type))],
            [self.preformatted_left('Semestre'), self.preformatted_right('Sem. {0}'.format(module.semestre))],
            [self.preformatted_left('Présentiel'),
                self.preformatted_right('{0} heures'.format(module.periode_presentiel))],
            [self.preformatted_left('Travail personnel'),
                self.preformatted_right('{0} heures'.format(module.travail_perso))],
            [self.preformatted_left('Responsable'),
                self.preformatted_right(module.processus.domaine.responsable.descr_pdf())],
        ]

        t = Table(data, colWidths=[3*cm, 13*cm])
        t.hAlign = TA_CENTER
        t.setStyle(
            TableStyle([
                ('SIZE', (0, 0), (-1, -1), 7),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 0), ]
            )
        )
        self.flowable.append(t)
        self.build(self.flowable)


class PlanFormationPdf(MyESDocTemplate):

    def __init__(self, filename):
        super().__init__(filename, ['Formation EDS', 'Plan de formation'], landscape(A4))

    def formating(self, el1='', length=40):
        el1 = '' if el1 == '' else el1.__str__()
        return Preformatted(el1, style_normal, maxLineLength=length)

    def produce(self, domain, process):
        # my_frame = Frame(2*cm, 1*cm, 26*cm, 15*cm, showBoundary=1)
        data = [
            ['Domaines', 'Processus', 'Sem1', 'Sem2', 'Sem3', 'Sem4', 'Sem5', 'Sem6'],
            [self.formating(domain[0]), self.formating(process[0], 60), 'M01', '', '', '', '', ''],
            [self.formating(''), self.formating('', 60), 'M02', '', '', '', '', ''],
            [self.formating(''), self.formating(process[1], 60), '', '', '', 'M03', '', ''],
            [self.formating(''), self.formating('', 60), '', 'M04', '', '', '', ''],
            [self.formating(domain[1]), self.formating(process[2], 60), 'M05', '', 'M06', '', '', ''],
            [self.formating(''), self.formating(process[3], 60), '', '', '', '', 'M07', 'M09'],
            [self.formating(''), self.formating('', 60), '', '', '', '', 'M08', ''],
            [self.formating(domain[2]), self.formating(process[4], 60), '', '', 'M10', '', 'M12'],
            [self.formating(''), self.formating(process[5], 60), '', '', 'M11', '', ''],
            [self.formating(domain[3]), self.formating(process[6], 60), '', '', 'M13', '', '', 'M14'],
            [self.formating(domain[4]), self.formating(process[7], 60), 'M15', '', '', '', '', ''],
            [self.formating(domain[5]), self.formating(process[8], 60), 'M16_1', '', 'M16_2', '', 'M16_3', ''],
            [self.formating(domain[6]), self.formating(process[9], 60), 'M17_1', '', 'M17_2', '', 'M17_3', ''],
            [self.formating(domain[7]), self.formating(process[10], 60), 'Macc', '', '', '', '', ''],
        ]
        t = Table(data, colWidths=[7*cm, 9*cm, 1.5*cm, 1.5*cm, 1.5*cm, 1.5*cm, 1.5*cm, 1.5*cm],
                  spaceBefore=0.5*cm, spaceAfter=1*cm)
        t.setStyle(TableStyle([
            ('SIZE', (0, 0), (-1, -1), 8),
            ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (2, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
            # Domaine 1
            ('SPAN', (0, 1), (0, 4)),
            ('SPAN', (1, 1), (1, 2)),
            ('SPAN', (1, 3), (1, 4)),
            ('BACKGROUND', (0, 1), (1, 4), colors.orange),
            ('BACKGROUND', (2, 1), (2, 2), colors.orange),
            ('BACKGROUND', (5, 3), (5, 3), colors.orange),
            ('BACKGROUND', (3, 4), (3, 4), colors.orange),
            # Domaine 2
            ('SPAN', (0, 5), (0, 7)),
            ('BACKGROUND', (0, 5), (1, 7), colors.red),
            ('BACKGROUND', (2, 5), (2, 5), colors.red),
            ('BACKGROUND', (4, 5), (4, 5), colors.red),
            ('BACKGROUND', (6, 6), (6, 6), colors.red),
            ('BACKGROUND', (7, 6), (7, 6), colors.red),
            ('BACKGROUND', (6, 7), (6, 7), colors.red),
            # Domaine 3
            ('SPAN', (0, 8), (0, 9)),
            ('SPAN', (1, 6), (1, 7)),
            ('SPAN', (4, 8), (5, 8)),
            ('SPAN', (4, 9), (5, 9)),
            ('BACKGROUND', (0, 8), (1, 9), colors.pink),
            ('BACKGROUND', (4, 8), (6, 8), colors.pink),
            ('BACKGROUND', (4, 9), (5, 9), colors.pink),
            # Domaine 4
            ('BACKGROUND', (0, 10), (1, 10), HexColor('#AD7FA8')),
            ('BACKGROUND', (4, 10), (4, 10), HexColor('#AD7FA8')),
            ('BACKGROUND', (7, 10), (7, 10), HexColor('#AD7FA8')),
            # Domaine 5
            ('SPAN', (2, 11), (-1, 11)),
            ('BACKGROUND', (0, 11), (-1, 11), HexColor('#729FCF')),
            # Domaine 6
            ('SPAN', (2, 12), (3, 12)),
            ('SPAN', (4, 12), (5, 12)),
            ('SPAN', (6, 12), (7, 12)),
            ('BACKGROUND', (0, 12), (-1, 12), colors.lightgreen),
            # Domaine 7
            ('SPAN', (2, 13), (3, 13)),
            ('SPAN', (4, 13), (5, 13)),
            ('SPAN', (6, 13), (7, 13)),
            ('BACKGROUND', (0, 13), (-1, 13), colors.white),
            # Domaine 8
            ('SPAN', (2, 14), (-1, 14)),
            ('BACKGROUND', (0, 14), (-1, 14), colors.lightgrey),

        ]))
        t.hAlign = TA_LEFT
        self.flowable.append(t)
        self.build(self.flowable)


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
        

class PeriodeFormationPdf(MyESDocTemplate):
    """Imprime les heures de cours par semestre"""
    def __init__(self, filename):
        super().__init__(filename, ['Filière EDS', 'Heures de formation'])

    def run(self):
        table_grid = [["Product", "Quantity"]]
        # Add the objects
        self.objects = ['col1', 'col2'] * 50
        for shipped_object in self.objects:
            table_grid.append([shipped_object, "42"])
        t = Table(table_grid, colWidths=[0.5 * self.width, 0.5 * self.width])
        t.setStyle(TableStyle([('GRID', (0, 1), (-1, -1), 0.25, colors.gray),
                               ('BOX', (0, 0), (-1, -1), 1.0, colors.black),
                               ('BOX', (0, 0), (1, 0), 1.0, colors.black),
                               ]))
        self.flowable.append(t)
        print(self.flowable)
        """
        self.flowable.append(Table(table_grid, repeatRows=1, colWidths=[0.5 * self.width, 0.5 * self.width],
                                   style=TableStyle([('GRID', (0, 1), (-1, -1), 0.25, colors.gray),
                                                     ('BOX', (0, 0), (-1, -1), 1.0, colors.black),
                                                     ('BOX', (0, 0), (1, 0), 1.0, colors.black),
                                                     ])))

        """
        self.build(self.flowable)

    def produce_half_year(self, half_year_id, modules, total):
        initial_pos_x = [2, 11.5]
        initial_pos_y = [17, 17, 10, 10, 3, 3]
        width = 7.5*cm
        height = 6.5*cm

        x = initial_pos_x[(half_year_id-1) % 2]*cm
        y = initial_pos_y[half_year_id-1]*cm

        my_frame = Frame(x, y, width, height, showBoundary=1)
        data = [['Semestre {0}'.format(half_year_id), '{0} h.'.format(total)]]
        for line in modules:
            value = getattr(line, 'sem{0}'.format(half_year_id))
            data.append([line.nom, '{0} h.'.format(value)])

        t = Table(data, colWidths=[7*cm, 1*cm], spaceBefore=0.5*cm, spaceAfter=1*cm, hAlign=TA_LEFT)
        t.setStyle(TableStyle([('ALIGN', (0, 0), (0, 0), 'LEFT'),
                               ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
                               ('LINEBELOW', (0, 0), (1, 0), 1, colors.black),
                               ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'), ]))

        self.flowable.append(t)
        my_frame.addFromList(self.flowable, self.canv)
        self.canv.save()

    def print_total(self, total):
        self.canv.drawString(2*cm, 2*cm, 'Total de la formation: {0} heures'.format(total))

