import os
import tempfile

from django.conf import settings
from django.contrib.staticfiles.finders import find

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.platypus import (Frame, FrameBreak, Flowable, NextPageTemplate,
                                Paragraph, PageTemplate, Preformatted, Spacer,
                                SimpleDocTemplate, Table, TableStyle
                                )

style_normal = ParagraphStyle(name='CORPS', fontName='Helvetica', fontSize=9, alignment=TA_LEFT)
style_bold = ParagraphStyle(name='CORPS', fontName='Helvetica-Bold', fontSize=10, alignment=TA_LEFT)
style_footer = ParagraphStyle(name='CORPS', fontName='Helvetica', fontSize=7, alignment=TA_CENTER)

LOGO_EPC = find('img/logo_EPC.png')
LOGO_ESNE = find('img/logo_ESNE.png')
LOGO_EPC_LONG = find('img/header.gif')


class HorLine(Flowable):
    """Horizontal Line flowable --- draws a line in a flowable"""

    def __init__(self, width):
        Flowable.__init__(self)
        self.width = width

    def __repr__(self):
        return "Line(w=%s)" % self.width

    def draw(self):
        self.canv.line(0, 0, self.width, 0)


class EpcBaseDocTemplate(SimpleDocTemplate):
    points = '.' * 93

    def __init__(self, filename, section='', subject='', orientation=A4):
        path = os.path.join(tempfile.gettempdir(), filename)
        super().__init__(
            path,
            pagesize=orientation,
            lefMargin=2.5 * cm, bottomMargin=1 * cm, topMargin=1 * cm, rightMargin=2.5 * cm
        )
        self.page_frame = Frame(
            self.leftMargin, self.bottomMargin, self.width - 2.5, self.height - 4 * cm,
            id='first_table', showBoundary=0, leftPadding=0 * cm
        )
        self.story = []
        self.section = section
        self.subject = subject

    def header(self, canvas, doc):
        # Logos
        canvas.saveState()
        canvas.drawImage(
            LOGO_EPC, doc.leftMargin, doc.height - 1.5 * cm, 5 * cm, 3 * cm, preserveAspectRatio=True
        )
        canvas.drawImage(
            LOGO_ESNE, doc.width - 2.5 * cm, doc.height - 1.2 * cm, 5 * cm, 3 * cm, preserveAspectRatio=True
        )

        # Section and subject
        x = doc.leftMargin
        y = doc.height - 2.5 * cm
        canvas.setFont('Helvetica-Bold', 10)
        canvas.line(x, y, x + doc.width, y)
        y -= 0.4 * cm
        canvas.drawString(x, y, self.section)
        canvas.drawRightString(x + doc.width, y, self.subject)
        y -= 0.2 * cm
        canvas.line(x, y, x + doc.width, y)

        # Footer
        canvas.line(doc.leftMargin, 1 * cm, doc.width + doc.leftMargin, 1 * cm)
        footer = Paragraph(settings.PDF_FOOTER_TEXT, style_footer)
        w, h = footer.wrap(doc.width, doc.bottomMargin)
        footer.drawOn(canvas, doc.leftMargin, h)
        canvas.restoreState()

    def later_header(self, canvas, doc):
        # Footer
        canvas.saveState()
        canvas.line(doc.leftMargin, 1 * cm, doc.width + doc.leftMargin, 1 * cm)
        footer = Paragraph(settings.PDF_FOOTER_TEXT, style_footer)
        w, h = footer.wrap(doc.width, doc.bottomMargin)
        footer.drawOn(canvas, doc.leftMargin, h)
        canvas.restoreState()

    def formating(self, text, len=25):
        return Preformatted(text, style_normal, maxLineLength=len)

    def normal_template_page(self):
        first_page_table_frame = Frame(self.leftMargin, self.bottomMargin, self.width + 1 * cm, self.height - 5 * cm,
                                       id='first_table', showBoundary=0, leftPadding=0 * cm)
        later_pages_table_frame = Frame(self.leftMargin, self.bottomMargin, self.width + 1 * cm, self.height - 5 * cm,
                                        id='later_table', showBoundary=0, leftPadding=0 * cm)
        # Page template
        first_page = PageTemplate(id='FirstPage', frames=[first_page_table_frame], onPage=self.header)
        later_pages = PageTemplate(id='LaterPages', frames=[later_pages_table_frame], onPage=self.header)
        self.addPageTemplates([first_page, later_pages])
        self.story = [NextPageTemplate(['*', 'LaterPages'])]

    def six_semester_template_page(self):
        frame_title = Frame(self.leftMargin, 24*cm, self.width, 1*cm, showBoundary=0, leftPadding=0)
        w, h = (7.5 * cm, 6.5 * cm,)

        x = [self.leftMargin, 11 * cm] * 3
        y = [17 * cm, 17 * cm, 10 * cm, 10 * cm, 3 * cm, 3 * cm]
        frames = [Frame(x[f], y[f], width=w, height=h, showBoundary=0, leftPadding=0) for f in range(6)]
        # Frame for total periods
        frames.append(Frame(self.leftMargin, self.bottomMargin, self.width, 1.5 * cm, leftPadding=0))
        frames.insert(0, frame_title)
        # Page template
        frame_page = PageTemplate(id='FirstPage', frames=frames, onPage=self.header)
        self.addPageTemplates(frame_page)


class NumberedCanvas(canvas.Canvas):
    """
    Page number and pages counter
    """
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
        self.drawString(self._pagesize[0] / 2, 1 * cm, "Page {0} de {1}".format(self._pageNumber, page_count))


class ModuleDescriptionPdf(EpcBaseDocTemplate):
    """
    PDF for module description
    """

    def __init__(self, filename):
        super().__init__(filename, 'Filière EDS', 'Module de formation')
        self.normal_template_page()

    def produce(self, module):

        str_competence = ' \n'.join(['- {0} ({1})'.format(c.nom, c.code) for c in module.competence_set.all()])

        str_sous_competence = ''
        for c in module.competence_set.all():
            for sc in c.souscompetence_set.all():
                str_sous_competence += '- {0} (voir {1})\n'.format(sc.nom, c.code)

        str_res = ' \n'.join(['- {0}'.format(c.nom) for c in module.ressource_set.all()])  # for future use

        str_objectif = ' \n'.join(['- {0}'.format(c.nom) for c in module.objectif_set.all()])

        self.story.append(Paragraph(module.__str__(), style_bold))
        self.story.append(Spacer(0, 0.5 * cm))

        data = [
                ['Domaine', module.processus.domaine.__str__()],
                ['Processus', module.processus.__str__()],
                ['Situation emblématique', module.situation],
                ['Compétences visées', str_competence],
                ['Plus-value sur le CFC ASE', str_sous_competence],
                ['Objectifs', str_objectif],
                ['Didactique', module.didactique],
                ['Evaluation', module.evaluation],
                ['Type', '{0}, obligatoire'.format(module.type)],
                ['Semestre', 'Sem. {0}'.format(module.semestre)],
                ['Présentiel', '{0} heures'.format(module.total_presentiel)],
                ['Travail personnel', '{0} heures'.format(module.travail_perso)],
                ['Responsable', module.processus.domaine.responsable.descr_pdf()]
            ]

        formated_data = []
        for foo in data:
            formated_data.append(
                [
                    Preformatted(foo[0], style_normal, maxLineLength=15),
                    Preformatted(foo[1], style_normal, maxLineLength=85),
                ]
            )

        t = Table(data=formated_data, colWidths=[4 * cm, 13 * cm])
        t.hAlign = TA_LEFT
        t.setStyle(tblstyle=TableStyle(
                [
                    ('SIZE', (0, 0), (-1, -1), 7),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ]
            )
        )
        self.story.append(t)
        self.build(self.story)


class FormationPlanPdf(EpcBaseDocTemplate):
    """
    PDF for formation plan
    """

    def __init__(self, filename):
        super().__init__(filename, 'Filière EDS', 'Plan de formation', landscape(A4))
        self.normal_template_page()

    def formating(self, el1='', length=40):
        el1 = '' if el1 == '' else el1.__str__()
        return Preformatted(el1, style_normal, maxLineLength=length)

    def produce(self, domain, process):
        print(domain[0], process[0])
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
            [self.formating(domain[3]), self.formating(process[6], 60), '', '', 'M13', '', 'M14', ''],
            [self.formating(domain[4]), self.formating(process[7], 60), 'M15', '', '', '', '', ''],
            [self.formating(domain[5]), self.formating(process[8], 60), 'M16_1', '', 'M16_2', '', 'M16_3', ''],
            [self.formating(domain[6]), self.formating(process[9], 60), 'M17_1', '', 'M17_2', '', 'M17_3', ''],
            [self.formating(domain[7]), self.formating(process[10], 60), 'Macc', '', '', '', '', ''],
        ]
        t = Table(
            data=data, colWidths=[7 * cm, 9 * cm, 1.5 * cm, 1.5 * cm, 1.5 * cm, 1.5 * cm, 1.5 * cm, 1.5 * cm],
            spaceBefore=0.5 * cm, spaceAfter=1 * cm
        )
        t.setStyle(tblstyle=TableStyle(
                [
                    ('SIZE', (0, 0), (-1, -1), 8),
                    ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('ALIGN', (2, 0), (-1, -1), 'CENTER'),
                    ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
                    # Domaine 1
                    ('SPAN', (0, 1), (0, 4)),
                    ('SPAN', (1, 1), (1, 2)),
                    ('SPAN', (1, 3), (1, 4)),
                    ('BACKGROUND', (0, 1), (1, 4), settings.DOMAINE_COULEURS['D1']),
                    ('BACKGROUND', (2, 1), (2, 2), settings.DOMAINE_COULEURS['D1']),
                    ('BACKGROUND', (5, 3), (5, 3), settings.DOMAINE_COULEURS['D1']),
                    ('BACKGROUND', (3, 4), (3, 4), settings.DOMAINE_COULEURS['D1']),
                    # Domaine 2
                    ('SPAN', (0, 5), (0, 7)),
                    ('BACKGROUND', (0, 5), (1, 7), settings.DOMAINE_COULEURS['D2']),
                    ('BACKGROUND', (2, 5), (2, 5), settings.DOMAINE_COULEURS['D2']),
                    ('BACKGROUND', (4, 5), (4, 5), settings.DOMAINE_COULEURS['D2']),
                    ('BACKGROUND', (6, 6), (6, 6), settings.DOMAINE_COULEURS['D2']),
                    ('BACKGROUND', (7, 6), (7, 6), settings.DOMAINE_COULEURS['D2']),
                    ('BACKGROUND', (6, 7), (6, 7), settings.DOMAINE_COULEURS['D2']),
                    # Domaine 3
                    ('SPAN', (0, 8), (0, 9)),
                    ('SPAN', (1, 6), (1, 7)),
                    ('SPAN', (4, 8), (5, 8)),
                    ('SPAN', (4, 9), (5, 9)),
                    ('BACKGROUND', (0, 8), (1, 9), settings.DOMAINE_COULEURS['D3']),
                    ('BACKGROUND', (4, 8), (6, 8), settings.DOMAINE_COULEURS['D3']),
                    ('BACKGROUND', (4, 9), (5, 9), settings.DOMAINE_COULEURS['D3']),
                    # Domaine 4
                    ('BACKGROUND', (0, 10), (1, 10), settings.DOMAINE_COULEURS['D4']),
                    ('BACKGROUND', (4, 10), (4, 10), settings.DOMAINE_COULEURS['D4']),
                    ('BACKGROUND', (6, 10), (6, 10), settings.DOMAINE_COULEURS['D4']),
                    # Domaine 5
                    ('SPAN', (2, 11), (-1, 11)),
                    ('BACKGROUND', (0, 11), (-1, 11), settings.DOMAINE_COULEURS['D5']),
                    # Domaine 6
                    ('SPAN', (2, 12), (3, 12)),
                    ('SPAN', (4, 12), (5, 12)),
                    ('SPAN', (6, 12), (7, 12)),
                    ('BACKGROUND', (0, 12), (-1, 12), settings.DOMAINE_COULEURS['D6']),
                    # Domaine 7
                    ('SPAN', (2, 13), (3, 13)),
                    ('SPAN', (4, 13), (5, 13)),
                    ('SPAN', (6, 13), (7, 13)),
                    ('BACKGROUND', (0, 13), (-1, 13), settings.DOMAINE_COULEURS['D7']),
                    # Domaine 8
                    ('SPAN', (2, 14), (-1, 14)),
                    ('BACKGROUND', (0, 14), (-1, 14), settings.DOMAINE_COULEURS['D8']),
                ]
            )
        )
        t.hAlign = TA_LEFT
        self.story.append(t)
        self.build(self.story)


class PeriodSemesterPdf(EpcBaseDocTemplate):
    """
    PDF for periods during semesters
    """

    def __init__(self, filename):
        super().__init__(filename, 'Filière EDS', 'Périodes de formation')
        self.six_semester_template_page()

    def produce(self, context):

        for sem in range(1, 7):
            modules = context['sem{0}'.format(str(sem))]
            total = context['tot{0}'.format(str(sem))]
            data = [['Semestre {0}'.format(sem), '{0} h.'.format(total)]]
            for line in modules:
                value = getattr(line, 'sem{0}'.format(sem))
                data.append([line.nom, '{0} h.'.format(value)])
            t = Table(data=data, colWidths=[6 * cm, 1 * cm], spaceBefore=0 * cm, spaceAfter=0.5 * cm, hAlign=TA_LEFT,
                      style=[
                                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                                ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
                                ('LINEBELOW', (0, 0), (1, 0), 1, colors.black),
                                ('SIZE', (0, 0), (-1, -1), 8),
                                ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ]
                      )
            self.story.append(t)
            self.story.append(FrameBreak())

        self.story.append(Paragraph('Total de la formation: {0} heures'.format(context['tot']), style_bold))
        self.build(self.story)
