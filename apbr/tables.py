import django_tables2 as tables
from django.utils.safestring import mark_safe
from django_tables2.utils import A

from utilities.tables import BaseTable, ChoiceFieldColumn, ToggleColumn, TagColumn

from .models import Apbr

AVAILABLE_LABEL = mark_safe('<span class="label label-success">Available</span>')
COL_TENANT = """
 {% if record.tenant %}
     <a href="{{ record.tenant.get_absolute_url }}" title="{{ record.tenant.description }}">{{ record.tenant }}</a>
 {% else %}
     &mdash;
 {% endif %}
 """

POLICIES = """
{% for rp in value.all %}
    <a href="{{ rp.get_absolute_url }}">{{ rp }}</a>{% if not forloop.last %}<br />{% endif %}
{% empty %}
    &mdash;
{% endfor %}
"""


class ApbrTable(BaseTable):
    pk = ToggleColumn()
    number = tables.LinkColumn(text=lambda record: record.__str__(), args=[A('pk')])
    status = ChoiceFieldColumn(
        default=AVAILABLE_LABEL
    )
    site = tables.LinkColumn()
    tenant = tables.TemplateColumn(
        template_code=COL_TENANT
    )

    class Meta(BaseTable.Meta):
        model = Apbr
        fields = ('pk', 'number', 'description', 'status')
