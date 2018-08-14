from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from cms.models import Module
# Create your models here.


class IntranetDoc(models.Model):
    AUTHORIZATION_CHOICES = {
        (0, 'aucun'),
        (1, 'étudiant'),
        (2, 'prof'),
        (3, 'admin')
    }

    doc = models.FileField(upload_to='intranet', unique=True)
    module = models.ForeignKey(Module, null=False, on_delete=models.PROTECT)
    published = models.BooleanField(default=True, blank=False)
    authorization = models.SmallIntegerField("autorisation", choices=AUTHORIZATION_CHOICES, default=0)

    class Meta:
        verbose_name = 'Intranet'
        verbose_name_plural = 'Intranet'

    def __str__(self):
        return self.doc.name


@receiver(pre_delete, sender=IntranetDoc)
def remove_file(**kwargs):
    instance = kwargs.get('instance')
    instance.doc.delete(save=False)


