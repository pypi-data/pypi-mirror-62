from django.db.models import Manager, Q
from aristotle_mdr.contrib.slots.manager import SimplePermsQueryset
from django.contrib.contenttypes.models import ContentType
from aristotle_mdr.contrib.custom_fields.constants import CUSTOM_FIELD_STATES


class CustomFieldQueryset(SimplePermsQueryset):
    perm_field_name = 'visibility'


class CustomValueQueryset(SimplePermsQueryset):
    perm_field_name = 'field__visibility'

    def with_content(self):
        """Restricts qs to only values with non blank content"""
        return self.filter(~Q(content=""))


class CustomValueManager(Manager):

    def get_queryset(self):
        return CustomValueQueryset(self.model, using=self._db)

    def get_for_item(self, concept):
        qs = self.get_queryset().filter(
            concept=concept,
        ).select_related('field')
        return qs

    def get_allowed_for_item(self, concept, fields):
        """
        Return the values for a list of fields
        Used with get_allowed_fields
        """
        qs = self.get_queryset().filter(
            concept=concept,
            field__in=fields
        ).select_related('field')
        return qs

    def get_item_allowed(self, concept, user):
        return self.get_queryset().filter(concept=concept).visible(user, concept.workgroup)


class CustomFieldManager(Manager):

    def get_queryset(self):
        return CustomFieldQueryset(self.model, using=self._db)

    def get_allowed_fields(self, concept, user):
        """Return the fields viewable on an item by a user.
        Only for viewing, not for editing
        """
        queryset = self.get_queryset().visible(user, concept.workgroup)

        if user.is_superuser:
            return queryset
        else:
            # Filter out the custom fields that are 'Hidden'
            return queryset.exclude(state=CUSTOM_FIELD_STATES.hidden)

    def get_for_model(self, model, user=None):
        """Return the fields for a given model.
           Used for editing screen"""
        ct = ContentType.objects.get_for_model(model)
        fil = Q(allowed_model__isnull=True) | Q(allowed_model=ct)

        queryset = self.get_queryset().filter(fil)
        if user is not None:
            if user.is_superuser:
                return queryset
            else:
                return queryset.visible(user).exclude(state=CUSTOM_FIELD_STATES.hidden)
        else:
            # Filter out the custom fields that are 'Hidden'
            return queryset.visible(user).exclude(state=CUSTOM_FIELD_STATES.hidden)
