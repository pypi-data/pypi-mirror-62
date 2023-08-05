from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import FieldDoesNotExist, ObjectDoesNotExist
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView

from aristotle_mdr.contrib.help.models import ConceptHelp, HelpPage
from aristotle_mdr.utils import fetch_metadata_apps, cloud_enabled


class AppHelpViewer(DetailView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.app_label:
            self.app = self.object.app_label
            try:
                context['app'] = apps.get_app_config(self.app)
            except LookupError:
                raise Http404
        return context


class AllHelpView(ListView):
    template_name = "aristotle_mdr_help/all_help.html"

    def get_queryset(self):
        return HelpPage.objects.filter(
            Q(app_label__in=fetch_metadata_apps()) |
            Q(app_label__isnull=True)
        )


class AllConceptHelpView(ListView):
    template_name = "aristotle_mdr_help/all_concept_help.html"

    def get_queryset(self):
        return ConceptHelp.objects.filter(
            Q(app_label__in=fetch_metadata_apps()) |
            Q(app_label__isnull=True)
        )


class ConceptAppHelpView(ListView):
    template_name = "aristotle_mdr_help/app_concept_help.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['app'] = apps.get_app_config(self.kwargs['app'])
        if self.kwargs['app'] not in fetch_metadata_apps():
            raise Http404
        return context

    def get_queryset(self, *args, **kwargs):
        return ConceptHelp.objects.filter(
            app_label__in=fetch_metadata_apps()
        ).filter(app_label=self.kwargs['app'])


class HelpView(AppHelpViewer):
    template_name = "aristotle_mdr_help/regular_help.html"
    model = HelpPage


class ConceptHelpView(AppHelpViewer):
    template_name = "aristotle_mdr_help/concept_help.html"

    def get_object(self, queryset=None):
        if self.kwargs['app'] not in fetch_metadata_apps():
            raise Http404
        app = self.kwargs['app']
        model = self.kwargs['model']
        return get_object_or_404(ConceptHelp, app_label=app, concept_type=model)

    def get_context_data(self, **kwargs):
        from aristotle_mdr.contrib.custom_fields.models import CustomField

        context = super().get_context_data(**kwargs)

        model = self.kwargs['model']

        ct = ContentType.objects.get(app_label=self.app, model=model)
        context['model'] = ct.model_class()
        custom_help = None

        if cloud_enabled():
            from aristotle_cloud.contrib.custom_help.models import CustomHelp
            custom_help = CustomHelp.objects.filter(content_type=ct).first()

        context['custom_help'] = custom_help

        context['custom_fields'] = CustomField.objects.filter(allowed_model=ct).exclude(help_text_long="")

        return context


class ConceptFieldHelpView(TemplateView):
    template_name = "aristotle_mdr_help/field_help.html"

    def get_context_data(self, **kwargs):

        app = self.kwargs['app']
        model = self.kwargs['model']
        field_name = self.kwargs['field_name']
        ct = get_object_or_404(ContentType, app_label=app, model=model)
        field = None

        if app not in fetch_metadata_apps():
            raise Http404

        try:
            field = ct.model_class()._meta.get_field(field_name)
        except FieldDoesNotExist:
            try:
                field = ct.model_class()._meta.get_field(field_name + "_set")
            except FieldDoesNotExist:
                pass

        kwargs.update({'field': field})
        self.cloud_help_handler(ct, field_name, kwargs)

        if not field:  # If the passed field name is not the model's field name, then this must be a CustomField...
            from aristotle_mdr.contrib.custom_fields.models import CustomField
            try:
                field = CustomField.objects.get(allowed_model=ct, name__iexact=field_name)
            except ObjectDoesNotExist:
                raise Http404
            kwargs.update({
                'custom_field': field,
                'field': field_name,
                'this_is_a_custom_field': True,
            })

        kwargs.update({
            'app': apps.get_app_config(app),
            'model_name': model,
            'model': ct.model_class(),
            'content_type': ct,
        })
        return super().get_context_data(**kwargs)

    @staticmethod
    def cloud_help_handler(ct, field_name, kwargs):
        """
        This static method checks the availability of Aristotle Cloud and
        updates the kwargs with the Custom Help object for a specific model.
        :param ct: Content Type (Model) name of the Help Object requested.
        :param field_name: Specific field name of the Content Type (Model).
        :param kwargs: key_word_arguments to be updated with the Custom Help required.
        """
        custom_help = None
        if cloud_enabled():
            from aristotle_cloud.contrib.custom_help.models import CustomHelp
            try:
                custom_help = ct.custom_help.field_help.get(field_name, None)
            except CustomHelp.DoesNotExist:
                pass
            kwargs.update({'custom_help': custom_help})
