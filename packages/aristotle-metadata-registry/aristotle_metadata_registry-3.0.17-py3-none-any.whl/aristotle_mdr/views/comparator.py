import json
from reversion.models import Version
from typing import Optional

from django.db.models import Model
from django.utils.functional import cached_property
from django.core.exceptions import PermissionDenied

from aristotle_mdr.forms import CompareConceptsForm
from aristotle_mdr.models import _concept
from aristotle_mdr.perms import user_can_view

from aristotle_mdr.views.tools import AristotleMetadataToolView
from aristotle_mdr.views.versions import ConceptVersionCompareBase


class MetadataComparison(ConceptVersionCompareBase, AristotleMetadataToolView):
    template_name = 'aristotle_mdr/actions/compare/compare_items.html'
    context: dict = {}

    def get_form(self):
        user = self.request.user
        qs = _concept.objects.visible(user)
        return CompareConceptsForm(self.request.GET, user=user, qs=qs)

    def load_version_json(self, first_version, second_version):
        versions = {'first': first_version, 'second': second_version}

        for key, version in versions.items():
            try:
                version = json.loads(version.serialized_data)
            except json.JSONDecodeError:
                return None

            if type(version) == list:
                self.comparing_different_formats = True
                # It's the old version, modify it
                version = version[0]['fields']
            versions[key] = version

        return {
            'earlier': versions['first'],
            'later': versions['second'],
            'reordered': False
        }

    @cached_property
    def has_same_base_model(self) -> Optional[bool]:
        concept_1 = self.get_version_1_concept()
        concept_2 = self.get_version_2_concept()
        if concept_1 and concept_2:
            return concept_1._meta.model == concept_2._meta.model
        return None

    def get_subitem_key(self, subitem_model):
        field_names = [f.name for f in subitem_model._meta.get_fields()]
        if 'order' in field_names:
            key = 'order'
        elif 'field' in field_names and self.has_same_base_model:
            key = 'field'
        elif 'field' in field_names and not self.has_same_base_model:
            key = 'name'
        else:
            key = 'id'
        return key

    def get_model(self, concept) -> Model:
        if self.has_same_base_model:
            return concept.item._meta.model

        return _concept

    def get_version_1_concept(self):
        form = self.get_form()
        if form.is_valid():
            # Get items from form
            item = form.cleaned_data['item_a'].item
            if user_can_view(self.request.user, item):
                return item
            else:
                raise PermissionDenied
        return None

    def get_version_2_concept(self):
        form = self.get_form()
        if form.is_valid():
            # Get items from form
            item = form.cleaned_data['item_b'].item
            if user_can_view(self.request.user, item):
                return item
            else:
                raise PermissionDenied
        return None

    def apply_permission_checking(self, version_permission_1, version_permission_2):
        # We're not checking the version permissions because we are getting the most
        # recent version and we have already checked that the user can view the item
        # so the 'content' viewed is the same.
        pass

    def get_compare_versions(self):
        concept_1 = self.get_version_1_concept()
        concept_2 = self.get_version_2_concept()

        if not concept_1 or not concept_2:
            self.context['not_all_versions_selected'] = True
            return None, None

        try:
            version_1 = Version.objects.get_for_object(concept_1).order_by('-revision__date_created').first().pk
            version_2 = Version.objects.get_for_object(concept_2).order_by('-revision__date_created').first().pk
        except AttributeError:
            self.context['cannot_compare'] = True
            return None, None

        return version_1, version_2

    def get_context_data(self, **kwargs):
        self.context = super().get_context_data(**kwargs)

        if self.get_version_1_concept() is None and self.get_version_2_concept() is None:
            # Not all concepts selected
            self.context['form'] = self.get_form()
            return self.context

        self.context.update({
            "form": self.get_form(),
            "has_same_base_model": self.has_same_base_model,
            "item_a": self.get_version_1_concept(),
            "item_b": self.get_version_2_concept(),
        })

        return self.context
