"""Django Model for tracking applications defined within an APBR policy."""

import logging

from django.urls import reverse
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.conf import settings

from taggit.managers import TaggableManager

from utilities.choices import ChoiceSet
from utilities.querysets import RestrictedQuerySet
from netbox.models import ChangeLoggedModel

from netbox.models import CustomFieldsMixin as CustomFieldModel

from extras.models import TaggedItem
from extras.utils import extras_features


LOGGER = logging.getLogger(__name__)


class ApbrStatusChoices(ChoiceSet):

    STATUS_ACTIVE = 'active'
    STATUS_RESERVED = 'reserved'
    STATUS_DEPRECATED = 'deprecated'

    CHOICES = (
        (STATUS_ACTIVE, 'Active'),
        (STATUS_RESERVED, 'Reserved'),
        (STATUS_DEPRECATED, 'Deprecated'),
    )

    CSS_CLASSES = {
        STATUS_ACTIVE: 'primary',
        STATUS_RESERVED: 'info',
        STATUS_DEPRECATED: 'danger',
    }


class ApbrGroup(ChangeLoggedModel):
    """
    """
    name = models.CharField(
        max_length=100
    )
    site = models.ForeignKey(
        to='dcim.Site',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    description = models.CharField(
        max_length=200,
        blank=True
    )

    def __str__(self):
        return self.name



class ApbrBase(ChangeLoggedModel):
    """
    """
    site = models.ForeignKey(
        to='dcim.Site',
        on_delete=models.PROTECT,
        related_name="%(class)s_related",
        blank=True,
        null=True
    )
    tenant = models.ForeignKey(
        to='tenancy.Tenant',
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )
    status = models.CharField(
        max_length=50,
        choices=ApbrStatusChoices,
        default=ApbrStatusChoices.STATUS_ACTIVE
    )
    role = models.ForeignKey(
        to='ipam.Role',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    description = models.CharField(
        max_length=200,
        blank=True
    )
    tags = TaggableManager(through=TaggedItem)

    objects = RestrictedQuerySet.as_manager()

    class Meta:
        abstract = True


class RuleBase(ChangeLoggedModel):
    """
    """
    site = models.ForeignKey(
        to='dcim.Site',
        on_delete=models.PROTECT,
        related_name="%(class)s_related",
        blank=True,
        null=True
    )
    tenant = models.ForeignKey(
        to='tenancy.Tenant',
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )
    status = models.CharField(
        max_length=50,
        choices=ApbrStatusChoices,
        default=ApbrStatusChoices.STATUS_ACTIVE
    )
    role = models.ForeignKey(
        to='ipam.Role',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    description = models.CharField(
        max_length=200,
        blank=True
    )
    match = models.CharField(
        max_length=200,
        blank=True
    )
    then = models.CharField(
        max_length=200,
        blank=True
    )
    tags = TaggableManager(through=TaggedItem)

    objects = RestrictedQuerySet.as_manager()

    class Meta:
        abstract = True


@extras_features('custom_fields', 'export_templates', 'webhooks')
class Apbr(RuleBase, CustomFieldModel):

    number = models.PositiveBigIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(4294967295)]
    )

    group = models.ForeignKey(
        ApbrGroup,
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )

    # clone_fields = ['description', 'status', 'tenant']

    class Meta:
        verbose_name_plural = 'APBR Profiles'
        constraints = [
            models.UniqueConstraint(
                fields=['number', 'tenant'],
                name='apbr_tenant'
            ),
            models.UniqueConstraint(
                fields=['number'],
                condition=models.Q(tenant=None),
                name='apbr'
            ),
        ]
        # unique_together = ['number', 'site', 'tenant']

    def get_status_class(self):
        return ApbrStatusChoices.CSS_CLASSES.get(self.status)

    def get_absolute_url(self):
        return reverse('plugins:apbr:apbr', args=[self.pk])

    def get_asdot(self):
        if self.number > 65535:
            return '{}.{}'.format(self.number // 65536, self.number % 65536)
        else:
            return str(self.number)

    def __str__(self):
        nb_settings = settings.PLUGINS_CONFIG.get('apbr', {})
        asdot = nb_settings.get('asdot', False)
        if asdot:
            return self.get_asdot()
        return str(self.number)
