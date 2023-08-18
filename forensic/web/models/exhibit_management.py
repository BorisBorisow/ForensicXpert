from django.db import models

from .base import DefaultToStringMixin


class ReportFieldModel(models.Model):
    denotation = models.CharField(max_length=4096)
    short = models.CharField(max_length=64)

    def __str__(self):
        return "%s (%s)" % (self.short, self.denotation)

    class Meta:
        ordering = ["denotation"]
        abstract = True


class ExhibitComponentType(DefaultToStringMixin, ReportFieldModel):
    pass


class ExhibitType(DefaultToStringMixin, ReportFieldModel):
    pass


class ExhibitDataImageType(DefaultToStringMixin, ReportFieldModel):
    pass
