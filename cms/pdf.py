
import os
from django.http.response import HttpResponse
from django.conf import settings
from reportlab.platypus import (SimpleDocTemplate, Spacer, Frame, Paragraph, Preformatted,
                                PageTemplate, NextPageTemplate, FrameBreak)
from reportlab.platypus import Table, TableStyle, Image
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle as ps
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib.styles import getSampleStyleSheet

style_8_c = ps(name='CORPS', fontName='Helvetica', fontSize=6, alignment=TA_CENTER)
style_normal = ps(name='CORPS', fontName='Helvetica', fontSize=9, alignment=TA_LEFT)
style_bold = ps(name='CORPS', fontName='Helvetica-Bold', fontSize=10, alignment=TA_LEFT)
style_title = ps(name='CORPS', fontName='Helvetica', fontSize=12, alignment=TA_LEFT)
style_adress = ps(name='CORPS', fontName='Helvetica', fontSize=10, alignment=TA_LEFT, leftIndent=300)

LOGO_EPC = os.path.join(settings.MEDIA_ROOT, 'logo_EPC.png')
LOGO_ESNE = os.path.join(settings.MEDIA_ROOT, 'logo_ESNE.png')

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.setFont("Helvetica", 7)
        self.drawRightString(20*cm, 2*cm, "Page %d de %d" % (self._pageNumber, page_count))


class EpcBaseDocTemplate(SimpleDocTemplate):
    def __init__(self, filename, titles=['', ''], pagesize=A4):
        super().__init__(filename, pagesize=pagesize, _pageBreakQuick=0, lefMargin=1.5 * cm, bottomMargin=1.5 * cm,
                         topMargin=1.5 * cm, rightMargin=1.5 * cm)
        self.story = []
        self.titles = titles

    def header(self, canvas, doc):
        canvas.saveState()
        canvas.drawImage(LOGO_EPC, doc.leftMargin, doc.height - 0.5 * cm, 5 * cm, 3 * cm, preserveAspectRatio=True)
        canvas.drawImage(LOGO_ESNE, doc.width - 2 * cm, doc.height - 0.5 * cm, 5 * cm, 3 * cm,
                         preserveAspectRatio=True)
        canvas.line(doc.leftMargin, doc.height - 0.5 * cm, doc.width+doc.leftMargin, doc.height - 0.5 * cm)
        canvas.drawString(doc.leftMargin, doc.height - 1.1 * cm, self.titles[0])
        canvas.drawRightString(doc.width+doc.leftMargin, doc.height - 1.1 * cm, self.titles[1])
        canvas.line(doc.leftMargin, doc.height - 1.3 * cm, doc.width+doc.leftMargin, doc.height - 1.3 * cm)
        canvas.restoreState()

    def setNormalTemplatePage(self):
        first_page_table_frame = Frame(self.leftMargin, self.bottomMargin, self.width + 1 * cm, self.height - 4 * cm,
                                       id='small_table', showBoundary=0, leftPadding=0 * cm)
        later_pages_table_frame = Frame(self.leftMargin, self.bottomMargin, self.width + 1 * cm, self.height - 2 * cm,
                                        id='large_table', showBoundary=0, leftPadding=0 * cm)
        first_page = PageTemplate(id='FirstPage', frames=[first_page_table_frame], onPage=self.header)
        later_pages = PageTemplate(id='LaterPages', frames=[later_pages_table_frame])
        self.addPageTemplates([first_page, later_pages])
        self.story = [NextPageTemplate(['*', 'LaterPages'])]

    def setSixSemestreTemplatePage(self):
        width = 8 * cm
        height = 6.5 * cm

        x = [self.leftMargin, 12 * cm] * 3
        y = [17*cm, 17*cm, 10*cm, 10*cm, 3*cm, 3*cm]
        frames = [Frame(x[f], y[f], width=width, height=height, showBoundary=0, leftPadding=0) for
                  f in range(6)]
        frames.append(Frame(self.leftMargin, self.bottomMargin, self.width, 1.5*cm, leftPadding=0))
        # Page template
        frame_page = PageTemplate(id='FirstPage', frames=frames, onPage=self.header)
        self.addPageTemplates(frame_page)


class ModulePdf(EpcBaseDocTemplate):

    def __init__(self, filename):
        super().__init__(filename, ['Formation EDS', 'Module de formation'], A4)
        self.setNormalTemplatePage()

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

        self.story.append(Paragraph(module.__str__(), style_bold))
        self.story.append(Spacer(0, 0.5 * cm))

        data = [
            ['Domaine', module.processus.domaine.__str__()],
            ['Processus', module.processus.__str__()],
            ['Situation emblématique', module.situation],
            ['Compétences visées', str_comp],
            ['Plus-value sur le CFC ASE', str_scom],
            ['Objectifs', str_obj],
            ['Didactique', module.didactique],
            ['Evaluation', module.evaluation],
            ['Type', '{0}, obligatoire'.format(module.type)],
            ['Semestre', 'Sem. {0}'.format(module.semestre)],
            ['Présentiel', '{0} heures'.format(module.periode_presentiel)],
            ['Travail personnel', '{0} heures'.format(module.travail_perso)],
            ['Responsable', module.processus.domaine.responsable.descr_pdf()]
        ]

        formated_data = []
        for foo in data:
            formated_data.append(
                [Preformatted(foo[0], style_normal, maxLineLength=15),
                 Preformatted(foo[1], style_normal, maxLineLength=97),
                 ]
            )

        t = Table(formated_data, colWidths=[4*cm, 13*cm])
        t.hAlign = TA_LEFT
        t.setStyle(
            TableStyle([
                ('SIZE', (0, 0), (-1, -1), 7),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 0), ]
            )
        )
        self.story.append(t)
        self.build(self.story, canvasmaker=NumberedCanvas)


class PlanFormationPdf(EpcBaseDocTemplate):

    def __init__(self, filename):
        super().__init__(filename, ['Formation EDS', 'Plan de formation'], landscape(A4))
        self.setNormalTemplatePage()

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
        self.story.append(t)
        self.build(self.story)


class PeriodeFormationPdf(EpcBaseDocTemplate):
    """Imprime les heures de cours par semestre"""
    def __init__(self, filename):
        super().__init__(filename, ['Filière EDS', 'Périodes de formation'], A4)
        self.setSixSemestreTemplatePage()

    def produce(self, context):
        for sem in range(1, 7):
            modules = context['sem{0}'.format(str(sem))]
            total = context['tot{0}'.format(str(sem))]
            data = [['Semestre {0}'.format(sem), '{0} h.'.format(total)]]
            for line in modules:
                value = getattr(line, 'sem{0}'.format(sem))
                data.append([line.nom, '{0} h.'.format(value)])
            t = Table(data, colWidths=[6.5*cm, 1*cm], spaceBefore=0.5*cm, spaceAfter=1*cm, hAlign=TA_LEFT)
            t.setStyle(TableStyle(
                    [
                        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
                        ('LINEBELOW', (0, 0), (1, 0), 1, colors.black),
                        ('SIZE', (0, 0), (-1, -1), 9),
                        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ]
                )
            )

            self.story.append(t)
            self.story.append(FrameBreak())
        self.story.append(Paragraph('Total de la formation: {0} heures'.format(context['tot']), style_bold))
        self.build(self.story)
