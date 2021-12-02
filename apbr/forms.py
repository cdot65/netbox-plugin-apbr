import re

from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from extras.models import Tag
from tenancy.models import Tenant
from dcim.models import Site
from utilities.forms import (
    BootstrapMixin, DynamicModelChoiceField,
    DynamicModelMultipleChoiceField, StaticSelect,
    StaticSelectMultiple, TagFilterField
)
from extras.forms import (
    CustomFieldModelForm, CustomFieldBulkEditForm
)

from .models import (Apbr, ApbrStatusChoices)


from django.forms.widgets import TextInput


class ApbrField(forms.CharField):
    '''
    Return int value, but allows to input dotted digit text
    '''

    def to_python(self, value):
        if not re.match(r'^\d+(\.\d+)?$', value):
            raise ValidationError('Invalid AS Number: {}'.format(value))       
        if '.' in value:
            if int(value.split('.')[0]) > 65535 or int(value.split('.')[1]) > 65535:
                raise ValidationError('Invalid AS Number: {}'.format(value))
            try:
                return int(value.split('.')[0]) * 65536 + int(value.split('.')[1])
            except ValueError:
                raise ValidationError('Invalid AS Number: {}'.format(value))
        try:
            return int(value)
        except ValueError:
            raise ValidationError('Invalid AS Number: {}'.format(value))


class ASdotInput(TextInput):
    def _format_value(self, value):
        if not value:
            return 0
        if type(value) is str:
            return value
        if int(value) > 65535:
            return '{}.{}'.format(value // 65536, value % 65536)
        else:
            return value

    def render(self, name, value, attrs=None, renderer=None):
        nb_settings = settings.PLUGINS_CONFIG.get('apbr', {})
        asdot = nb_settings.get('asdot', False)
        if asdot:
            value = self._format_value(value)
        return super().render(name, value, attrs, renderer)


class ApbrFilterForm(BootstrapMixin, CustomFieldModelForm):
    q = forms.CharField(
        required=False,
        label='Search'
    )
    tenant = DynamicModelChoiceField(
        queryset=Tenant.objects.all(),
        required=False
    )
    status = forms.MultipleChoiceField(
        choices=ApbrStatusChoices,
        required=False,
        widget=StaticSelectMultiple()
    )
    site = DynamicModelChoiceField(
        queryset=Site.objects.all(),
        required=False
    )

    tag = TagFilterField(Apbr)

    class Meta:
        model = Apbr
        fields = ['q', 'status', 'tenant']


class ApbrForm(BootstrapMixin, CustomFieldModelForm):
    number = ApbrField(
        widget=ASdotInput
    )
    tags = DynamicModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False
    )
    site = DynamicModelChoiceField(
        queryset=Site.objects.all(),
        required=False
    )
    tenant = DynamicModelChoiceField(
        queryset=Tenant.objects.all(),
        required=False
    )

    def clean(self):
        cleaned_data = super().clean()
        if self.errors.get('number'):
            return cleaned_data
        number = cleaned_data.get('number')
        tenant = cleaned_data.get('tenant')
        if 'number' in self.changed_data or 'tenant' in self.changed_data:
            if Apbr.objects.filter(number=number, tenant=tenant).exists():
                raise forms.ValidationError('AS number with this number and tenant is already exists.')
        return cleaned_data

    class Meta:
        model = Apbr
        fields = [
            'number', 'description', 'status', 'site', 'tenant', 'tags', 'match', 'then',
        ]


class ApbrBulkEditForm(CustomFieldBulkEditForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=Apbr.objects.all(),
        widget=forms.MultipleHiddenInput
    )
    tenant = DynamicModelChoiceField(
        queryset=Tenant.objects.all(),
        required=False
    )
    description = forms.CharField(
        max_length=200,
        required=False
    )
    status = forms.ChoiceField(
        required=False,
        choices=ApbrStatusChoices,
        widget=StaticSelect()
    )

    class Meta:
        nullable_fields = [
            'tenant', 'description',
        ]
