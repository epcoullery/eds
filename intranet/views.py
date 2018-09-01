from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from cms.models import Module
from intranet.models import IntranetDoc


class IntranetListView(LoginRequiredMixin, ListView):
    model = IntranetDoc
    template_name = 'intranet/list.html'
    login_url = '/login/'

    def get_queryset(self):
        groups = self.request.user.groups.values_list('name',flat=True)
        qs = IntranetDoc.objects.filter(module=self.kwargs['module'], published=True)
        if self.request.user.is_superuser:
            qs = qs.filter(authorization__in=[1,2,3])
        elif 'prof' in groups:
            qs = qs.filter(authorization__in=[1,2])
        elif 'Student_1_year' in groups or 'Student_2_year' in groups or 'Student_3_year' in groups:
            modules = Module.objects.all().order_by('code')
            modules_selected = []
            student_access = {
                'Student_1_year': [m for m in modules if m.sem1 > 0 or m.sem2 > 0],
                'Student_2_year': [m for m in modules if m.sem3 > 0 or m.sem4 > 0],
                'Student_3_year': [m for m in modules if m.sem5 > 0 or m.sem6 > 0],
            }
            for group in groups:
                for mod in student_access[group]:
                    modules_selected.append(mod.code)
            qs = qs.filter(module__code__in=modules_selected, authorization=1)
        else:
            qs = qs.none()
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = get_object_or_404(Module, pk=self.kwargs['module'])
        return context
