import os

from django.conf import settings
from django.contrib import admin

from intranet.models import IntranetDoc


@admin.register(IntranetDoc)
class IntranetDocAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'module', 'authorization')

    def save_model(self, request, obj, form, change):
        searched_file = 'intranet/{0}'.format(form.cleaned_data['doc'])
        try:
            doc = IntranetDoc.objects.get(doc=searched_file)
            form.save()
            # Override previous file
            filename = os.path.join(settings.MEDIA_ROOT, searched_file)
            file = request.FILES['doc']
            with open(filename, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
        except IntranetDoc.DoesNotExist:
            super().save_model(request, obj, form, change)
