from django import forms
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext_lazy as _
from aristotle_mdr import models as MDR
from aristotle_mdr.contrib.slots.models import Slot
from aristotle_mdr.forms.bulk_actions import LoggedInBulkActionForm


def slot_inlineformset_factory():
    base_formset = inlineformset_factory(
        MDR._concept, Slot,
        can_delete=True,
        fields=('concept', 'name', 'type', 'value', 'order', 'permission'),
        extra=0,
        widgets={'order': forms.widgets.HiddenInput(), 'value': forms.widgets.Textarea({'cols': 20, 'rows': 5})}
    )

    return base_formset


class BulkAssignSlotsForm(LoggedInBulkActionForm):
    classes = "fa-tags"
    action_text = _('Bulk add slots')
    items_label = "Add slot details to multiple metadata items"
    confirm_page = "aristotle_mdr/slots/bulk_actions/add_slots.html"

    slot_name = forms.CharField(
        label=_("Slot name"),
        required=False,
    )
    slot_type = forms.CharField(
        label=_("Slot type"),
        required=False,
    )
    value = forms.CharField(
        required=True,
        label=_("The value to save"),
    )

    def make_changes(self):
        items = self.items_to_change
        # In this method check the user has permission to edit the items
        slot_name = self.cleaned_data.get('slot_name')
        slot_type = self.cleaned_data.get('slot_type')

        # Then check they are all the same type and can have the requested slot
        # Then save everything
        value = self.cleaned_data.get('value')
        for item in items:
            Slot.objects.create(concept=item, name=slot_name, type=slot_type, value=value)
        return _('%(num_items)s items have had slots assigned') % {'num_items': len(items)}
