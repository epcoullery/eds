
from django.http.response import HttpResponse
from django.conf import settings

from reportlab.platypus import SimpleDocTemplate, Spacer, Frame, Paragraph, Preformatted
from reportlab.platypus import Table, TableStyle, Image
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle as ps
from reportlab.pdfgen import canvas

style_8_c = ps(name='CORPS', fontName='Helvetica', fontSize=6, alignment=TA_CENTER)
style_normal = ps(name='CORPS', fontName='Helvetica', fontSize=9, alignment=TA_LEFT)
style_bold = ps(name='CORPS', fontName='Helvetica-Bold', fontSize=10, alignment=TA_LEFT, leftIndent=0.3*cm)
style_title = ps(name='CORPS', fontName='Helvetica', fontSize=12, alignment=TA_LEFT)
style_adress = ps(name='CORPS', fontName='Helvetica', fontSize=10, alignment=TA_LEFT, leftIndent=300)


class MyDocTemplateES(SimpleDocTemplate):
    def __init__(self, filename, title_left, title_right, portrait=True):
        if portrait is True:
            page_size = A4
            column_width = 8 * cm
        else:
            page_size = landscape(A4)
            column_width = 13 * cm
        SimpleDocTemplate.__init__(self, filename, pagesize=page_size,
                                   topMargin=0 * cm,
                                   leftMargin=2 * cm,
                                   rightMargin=2 * cm,
                                   bottomMargin=0.5 * cm,
                                   )
        self.fileName = filename
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

    def beforePage(self):
        # page number
        self.canv.saveState()
        self.canv.setFontSize(8)
        self.canv.drawCentredString(self.pagesize[0] / 2, 0.5 * cm, "Page : " + str(self.canv.getPageNumber()))
        self.canv.restoreState()


class ModulePdf(MyDocTemplateES):

    def __init__(self, filename):
        self.flowable = list()
        MyDocTemplateES.__init__(self, filename, 'Formation EDS', 'Module de formation', portrait=True)

    def preformatted_left(self, txt):
        return Preformatted(txt, style_normal, maxLineLength=15)

    def preformatted_right(self, txt):
        return Preformatted(txt, style_normal, maxLineLength=90)

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

        self.flowable.append(Spacer(0, 0.5 * cm))
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
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 0), ]
            )
        )
        self.flowable.append(t)
        self.build(self.flowable)


class PlanFormationPdf(MyDocTemplateES):

    def __init__(self, filename):
        self.flowable = list()
        MyDocTemplateES.__init__(self, filename, 'Formation EDS', 'Plan de formation', portrait=False)

    def formating(self, el1='', length=40):
        el1 = '' if el1 == '' else el1.__str__()
        return Preformatted(el1, style_normal, maxLineLength=length)

    def produce(self, domain, process):
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
        t.hAlign = TA_CENTER
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
        

class PeriodeFormationPdf(SimpleDocTemplate):
    """Imprime les heures de cours par semestre"""
    def __init__(self, filename):
        self.flowable = list()
        #SimpleDocTemplate.__init__(self, filename) #, 'Formation EDS', 'Périodes de la formation', portrait=True)
        c = canvas.Canvas(filename, pagesize=A4)
        width, height = A4
        im1 = Image(settings.MEDIA_ROOT + 'logo_EPC.png', width=120, height=80)
        im2 = Image(settings.MEDIA_ROOT + 'logo_ESNE.png', width=120, height=80)
        c.drawImage(settings.MEDIA_ROOT + 'logo_EPC.png', 0, height - 1*cm)  # Who needs consistency?
        c.drawImage(settings.MEDIA_ROOT + 'logo_ESNE.png', 8*cm, height-1*cm)
        c.showPage()
        c.save()


    def produce_half_year(self, half_year_id, modules, total, canv):
        initial_pos_x = [2, 11]
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

        t = Table(data, colWidths=[7*cm, 1*cm], spaceBefore=0, spaceAfter=0, hAlign=TA_LEFT)
        t.setStyle(TableStyle([('ALIGN', (0, 0), (0, 0), 'LEFT'),
                               ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
                               ('LINEBELOW', (0, 0), (1, 0), 1, colors.black),
                               ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'), ]))

        self.flowable.append(t)
        my_frame.addFromList(self.flowable, canv)
        # self.build(self.flowable)

    def print_total(self, total, canv):
        canv.drawString(2*cm, 2*cm, 'Total de la formation: {0} heures'.format(total))
