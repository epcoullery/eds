from django.conf import settings
from django.views.generic import ListView
from cms.models import Module
from intranet.models import IntranetDoc
from django.contrib.auth.mixins import LoginRequiredMixin


class IntranetListView(LoginRequiredMixin, ListView):

    model = IntranetDoc
    template_name = 'intranet/list.html'
    login_url = '/login/'
    redirect_field_name = 'redirecto_to'

    def get_queryset(self):
        modules = Module.objects.all().order_by('code')
        groups = self.request.user.groups.values_list('name',flat=True)

        if self.request.user.is_superuser:
            return IntranetDoc.objects.filter(authorization__in=[1,2,3],
                                              published=True)
        if 'prof' in groups:
            return IntranetDoc.objects.filter(authorization__in=[1,2],
                                              published=True)
        if 'Student_1_year' in groups or 'Student_2_year' in groups or 'Student_3_year' in groups:
            modules_selected = []
            student_access = {'Student_1_year': [m for m in modules if m.sem1 > 0 or m.sem2 > 0],
                              'Student_2_year': [m for m in modules if m.sem3 > 0 or m.sem4 > 0],
                              'Student_3_year': [m for m in modules if m.sem5 > 0 or m.sem6 > 0]
                              }


            for group in groups:
                for mod in student_access[group]: #settings.STUDENT_ACCESS[group]:
                    modules_selected.append(mod.code)
            return IntranetDoc.objects.filter(module__code__in=modules_selected,
                                              authorization=1,
                                              published=True)
        return None
