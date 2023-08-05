import haystack.indexes as indexes

from aristotle_mdr.contrib.help import models
from django.utils import timezone
from aristotle_mdr.search_indexes import (
    BaseObjectIndex,
    RESTRICTION,
    SEARCH_CATEGORIES,
)


class HelpObjectIndex(BaseObjectIndex):
    name = indexes.CharField(model_attr='title')
    name_sortable = indexes.CharField(model_attr='title', indexed=False, stored=True)
    is_public = indexes.BooleanField(model_attr='is_public')

    restriction = indexes.IntegerField(faceted=True)
    search_category = SEARCH_CATEGORIES.help

    def get_model(self):
        raise NotImplementedError  # pragma: no cover -- This should always be overridden

    # From http://unfoldthat.com/2011/05/05/search-with-row-level-permissions.html
    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""

        return self.get_model().objects.filter(modified__lte=timezone.now())

    def prepare_restriction(self, obj):
        return RESTRICTION['Public']

    def prepare(self, obj):
        # Slightly down-rank help in search
        data = super().prepare(obj)
        data['boost'] = 0.95
        return data


class ConceptHelpIndex(HelpObjectIndex, indexes.Indexable):
    template_name = "search/searchConceptHelp.html"

    def get_model(self):
        return models.ConceptHelp


class HelpPageIndex(HelpObjectIndex, indexes.Indexable):
    template_name = "search/searchHelpPage.html"

    def get_model(self):
        return models.HelpPage
