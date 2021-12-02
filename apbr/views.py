from netbox.views import generic

from .filters import ApbrFilterSet
from .models import Apbr
from .tables import ApbrTable
from .forms import ApbrFilterForm, ApbrBulkEditForm, ApbrForm


class ApbrListView(generic.ObjectListView):
    queryset = Apbr.objects.all()
    filterset = ApbrFilterSet
    filterset_form = ApbrFilterForm
    table = ApbrTable
    action_buttons = ()
    template_name = 'apbr/apbr_list.html'


class ApbrView(generic.ObjectView):
    queryset = Apbr.objects.all()
    template_name = 'apbr/apbr.html'


class ApbrEditView(generic.ObjectEditView):
    queryset = Apbr.objects.all()
    model_form = ApbrForm
    default_return_url = 'plugins:apbr:apbr_list'


class ApbrBulkDeleteView(generic.BulkDeleteView):
    queryset = Apbr.objects.all()
    table = ApbrTable


class ApbrBulkEditView(generic.BulkEditView):
    queryset = Apbr.objects.all()
    filterset = ApbrFilterSet
    table = ApbrTable
    form = ApbrBulkEditForm


class ApbrDeleteView(generic.ObjectDeleteView):
    queryset = Apbr.objects.all()
