from django.db import models
from django.db.models import JSONField, ManyToManyField
from django.utils.translation import gettext_lazy as _

from .base import DefaultToStringMixin, MainModel
from .exhibit_management import (
    ExhibitComponentType,
    ExhibitDataImageType,
    ExhibitType,
)
from .mandate import MandateRelatedMixin


class MainModelMandated(MandateRelatedMixin, MainModel):
    class Meta:
        abstract = True


class Exhibit(DefaultToStringMixin, MainModelMandated):
    denotation = models.CharField(max_length=4096)
    exhibit_type = models.ForeignKey(ExhibitType, on_delete=models.DO_NOTHING)
    serial_number = models.CharField(max_length=128, blank=True, null=True)

    handover_certificate_position_number = models.CharField(max_length=16, blank=True, null=True)
    handover_certificate_police_number = models.CharField(max_length=128, blank=True, null=True)
    handover_certificate_police_denotation = models.CharField(max_length=4096, blank=True, null=True)

    comments = models.CharField(max_length=16 * 65536, blank=True, null=True)
    description = models.CharField(max_length=16 * 65536, null=True, blank=True)

    excluded = models.BooleanField(default=False)

    state = models.CharField(max_length=30)

    class Meta:
        constraints = [
            # models.CheckConstraint(check=models.Q(exhibit_confiscate_certificate__isnull=False)
            #                              | models.Q(exhibit_handover_certificate__isnull=False),
            #                        name='incoming_certificate'),
            models.UniqueConstraint(fields=['denotation', 'mandate'],
                                    name="denotation_exhibit_unique_by_mandate")
        ]
        ordering = ["denotation"]


class ExhibitComponent(DefaultToStringMixin, MainModelMandated):
    denotation = models.CharField(max_length=1024)
    description = models.CharField(max_length=65536, blank=True, null=True)
    description_future = JSONField(blank=True, default=dict)
    capacity = models.BigIntegerField(null=True)
    serial_number = models.CharField(max_length=128, blank=True, null=True)
    comments = models.CharField(max_length=65536, blank=True, null=True)
    excluded = models.BooleanField(default=False)

    additional_parts = models.CharField(max_length=65536, null=True, blank=True)

    component_typ = models.ForeignKey(ExhibitComponentType, on_delete=models.DO_NOTHING)

    exhibit = models.ForeignKey(Exhibit, on_delete=models.DO_NOTHING)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['denotation', 'mandate'],
                                    name="denotation_exhibit_component_unique_by_mandate")
        ]
        ordering = ["denotation"]

    state = models.CharField(max_length=30)


class ExhibitDataImage(DefaultToStringMixin, MainModelMandated):
    denotation = models.CharField(max_length=64)
    comments = models.CharField(max_length=16 * 65536, blank=True, null=True)
    description = models.CharField(max_length=16 * 65536, null=True, blank=True)

    md5_sum = models.CharField(max_length=4096, null=True)
    size = models.BigIntegerField(null=True)
    image_type = models.ForeignKey(ExhibitDataImageType, on_delete=models.DO_NOTHING)

    main_exhibit_component = models.ForeignKey(ExhibitComponent, on_delete=models.DO_NOTHING, null=False, blank=False,
                                               related_name="mainexhibitdataimge_set")
    exhibit_component = ManyToManyField(
        ExhibitComponent, verbose_name=_('backend_exhibitdataimage_exhibit_component_verbose_name'), blank=True)
