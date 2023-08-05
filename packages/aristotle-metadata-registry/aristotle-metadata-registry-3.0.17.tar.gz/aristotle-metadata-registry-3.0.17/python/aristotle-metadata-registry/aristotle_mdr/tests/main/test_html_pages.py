from typing import Type
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.db.models.fields import CharField, TextField
from django.http import HttpResponse
from django.test import TestCase, override_settings, tag, RequestFactory
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model

import aristotle_mdr.models as MDR
import aristotle_mdr.perms as perms
import aristotle_mdr.contrib.identifiers.models as ident_models
from aristotle_mdr.constants import visibility_permission_choices as permission_choices
from aristotle_mdr.contrib.custom_fields.models import CustomField, CustomValue
from aristotle_mdr.utils import url_slugify_concept
from aristotle_mdr.forms.creation_wizards import (
    WorkgroupVerificationMixin,
    CheckIfModifiedMixin
)
from aristotle_mdr.tests import utils
from aristotle_mdr.views import ConceptRenderView
from aristotle_mdr.utils.versions import VersionLinkField
from aristotle_mdr.downloader import HTMLDownloader
from aristotle_mdr.tests.utils import model_to_dict_with_change_time

import datetime
from unittest import mock, skip
import reversion
from reversion import models as revmodels
import json
from freezegun import freeze_time


class AnonymousUserViewingThePages(TestCase):
    def test_homepage(self):
        response = self.client.get(reverse('aristotle:smart_root'))
        self.assertRedirects(response, reverse('aristotle:home'))

    def test_notifications_for_anon_users(self):
        response = self.client.get(reverse('aristotle:home'))
        self.assertEqual(response.status_code, 200)
        # Make sure notifications library isn't loaded for anon users as they'll never have notifications.
        self.assertNotContains(response, "notifications/notify.js")

    def test_sitemaps(self):
        response = self.client.get("/sitemap.xml")
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/sitemaps/sitemap_0.xml")
        self.assertEqual(response.status_code, 200)

    def test_visible_item(self):
        steward_org = MDR.StewardOrganisation.objects.create(name="Test SO")
        wg = MDR.Workgroup.objects.create(name="Setup WG", stewardship_organisation=steward_org)
        ra = MDR.RegistrationAuthority.objects.create(name="Test RA", stewardship_organisation=steward_org)
        item = MDR.ObjectClass.objects.create(name="Test OC", workgroup=wg)
        s = MDR.Status.objects.create(
            concept=item,
            registrationAuthority=ra,
            registrationDate=timezone.now(),
            state=ra.locked_state
        )
        response = self.client.get(url_slugify_concept(item))
        # Anonymous users requesting a hidden page will be redirected to login
        self.assertEqual(response.status_code, 302)
        s.state = ra.public_state
        s.save()
        response = self.client.get(url_slugify_concept(item))
        self.assertEqual(response.status_code, 200)


class LoggedInViewHTMLPages(utils.LoggedInViewPages, TestCase):
    def test_homepage(self):
        self.login_editor()
        response = self.client.get(reverse('aristotle:smart_root'))
        self.assertRedirects(response, reverse('aristotle:userHome'))


# Tests that dont require running on all item types
@tag('itempage_general')
class GeneralItemPageTestCase(utils.AristotleTestUtils, TestCase):

    def setUp(self):
        super().setUp()

        self.item = MDR.ObjectClass.objects.create(
            name='Test Item',
            definition='Test Item Description',
            submitter=self.editor,
            workgroup=self.wg1
        )
        self.itemid = self.item.id

        self.future_time = timezone.now() + datetime.timedelta(days=30)

        self.cache_key = 'view_cache_ConceptView_{}_{}'.format(
            self.editor.id,
            self.itemid
        )

        self.factory = RequestFactory()

        cache.clear()

    def setup_custom_values(self):
        allfield = CustomField.objects.create(
            order=0,
            name='AllField',
            type='String',
            visibility=permission_choices.public
        )
        authfield = CustomField.objects.create(
            order=1,
            name='AuthField',
            type='String',
            visibility=permission_choices.auth
        )
        wgfield = CustomField.objects.create(
            order=2,
            name='WgField',
            type='String',
            visibility=permission_choices.workgroup
        )
        self.allval = CustomValue.objects.create(
            field=allfield,
            content='All Value',
            concept=self.item
        )
        self.authval = CustomValue.objects.create(
            field=authfield,
            content='Auth Value',
            concept=self.item
        )
        self.wgval = CustomValue.objects.create(
            field=wgfield,
            content='Workgroup Value',
            concept=self.item
        )

    def create_versions(self):
        with reversion.create_revision():
            self.item.definition = 'New Definition'
            self.item.save()

        with reversion.create_revision():
            self.item.definition = 'Even newer Definition'
            self.item.save()

        versions = reversion.models.Version.objects.get_for_object(self.item)
        return versions

    def test_itempage_full_url(self):
        self.login_editor()
        full_url = url_slugify_concept(self.item)
        response = self.client.get(full_url)
        self.assertEqual(response.status_code, 200)

    def test_itempage_redirect_id_only(self):
        self.login_editor()

        response = self.reverse_get(
            'aristotle:item',
            reverse_args=[self.itemid],
            status_code=302
        )

        self.assertEqual(response.url, url_slugify_concept(self.item))

    def test_itempage_redirect_wrong_modelslug(self):
        self.login_editor()

        response = self.reverse_get(
            'aristotle:item',
            reverse_args=[self.itemid, 'definition', 'wow'],
            status_code=302
        )

        self.assertEqual(response.url, url_slugify_concept(self.item))

    def test_itempage_wrong_model_modelslug(self):
        self.login_editor()

        response = self.reverse_get(
            'aristotle:item',
            reverse_args=[self.itemid, 'property', 'wow'],
            status_code=302
        )
        self.assertEqual(response.url, url_slugify_concept(self.item))

    def test_itempage_wrong_name(self):
        self.login_editor()

        response = self.reverse_get(
            'aristotle:item',
            reverse_args=[self.itemid, 'objectclass', 'wow'],
            status_code=200
        )

    def test_registering_item_in_future_does_not_immediately_apply_status(self):
        """Test that registering item in future does not apply the status immediately"""
        ra = MDR.RegistrationAuthority.objects.create(name="Registration Authority",
                                                      stewardship_organisation=self.steward_org_1)
        """Test that registering an item in the future does not make it public immediately"""
        item = MDR.ObjectClass.objects.create(name="Object Class",
                                              definition="Object Class")
        MDR.Status.objects.create(concept=item,
                                  registrationAuthority=ra,
                                  registrationDate=datetime.datetime.now() + datetime.timedelta(weeks=52),
                                  state=MDR.STATES.standard,
                                  changeDetails="I changed this because I wanted to")
        self.logout()
        response = self.client.get(item.get_absolute_url())

        self.assertResponseStatusCodeEqual(response=response, code=302)  # redirect to friendly login
        self.login_superuser()
        response = self.client.get(item.get_absolute_url())
        self.assertContainsHtml(response, 'Not endorsed')

    def test_registering_item_in_future_becomes_public_after_registration_date_elapses(self):
        """Test that registering an item and then jumping Back to the Future™ the registration status has been
        applied. This doesn't exactly match the behaviour present in reality, because the recaching of item states is
         run by a celery scheduler """
        ra = MDR.RegistrationAuthority.objects.create(name="Registration Authority",
                                                      stewardship_organisation=self.steward_org_1)
        item = MDR.ObjectClass.objects.create(name="Object Class",
                                              definition="Object Class")
        # Register item in the future
        MDR.Status.objects.create(concept=item,
                                  registrationAuthority=ra,
                                  registrationDate=datetime.datetime.now() + datetime.timedelta(weeks=52),
                                  state=MDR.STATES.standard,
                                  changeDetails="I changed this because I wanted to")
        self.logout()
        # Go to the future
        with freeze_time((datetime.datetime.now() + datetime.timedelta(weeks=104)).strftime("%Y-%m-%d")):
            item.refresh_from_db()
            item.recache_states()
            response = self.client.get(item.get_absolute_url())
            self.assertResponseStatusCodeEqual(response=response, code=200)

    @tag('cache')
    @override_settings(CACHE_ITEM_PAGE=True)
    @skip('Cache mixin not currently used')
    def test_itempage_caches(self):
        # View in the future to avoid modified recently check
        # No flux capacitors required
        with mock.patch('aristotle_mdr.utils.utils.timezone.now') as mock_now:
            mock_now.return_value = self.future_time

            self.login_editor()
            response = self.reverse_get(
                'aristotle:item',
                reverse_args=[self.itemid, 'objectclass', 'test-item'],
                status_code=200
            )

        cached_itempage = cache.get(self.cache_key, None)
        self.assertIsNotNone(cached_itempage)

    @tag('cache')
    @override_settings(CACHE_ITEM_PAGE=True)
    @skip('Cache mixin not currently used')
    def test_itempage_loaded_from_cache(self):
        # Load response into cache
        cache.set(self.cache_key, HttpResponse('wow'))

        # View item page in future
        with mock.patch('aristotle_mdr.utils.utils.timezone.now') as mock_now:
            mock_now.return_value = self.future_time

            self.login_editor()
            response = self.reverse_get(
                'aristotle:item',
                reverse_args=[self.itemid, 'objectclass', 'test-item'],
                status_code=200
            )

            self.assertEqual(response.content, b'wow')

    @tag('cache')
    @override_settings(CACHE_ITEM_PAGE=True)
    @skip('Cache mixin not currently used')
    def test_itempage_not_loaded_from_cache_if_modified(self):
        # Load response into cache
        cache.set(self.cache_key, HttpResponse('wow'))

        # View page now (assumes this test wont take 300 seconds)
        self.login_editor()
        response = self.reverse_get(
            'aristotle:item',
            reverse_args=[self.itemid, 'objectclass', 'test-item'],
            status_code=200
        )

        self.assertNotEqual(response.content, b'wow')

    @tag('cache')
    @override_settings(CACHE_ITEM_PAGE=True)
    @skip('Cache mixin not currently used')
    def test_itempage_not_loaded_from_cache_if_nocache_set(self):
        cache.set(self.cache_key, HttpResponse('wow'))

        url = reverse('aristotle:item', args=[self.itemid, 'objectclass', 'test-item'])
        url += '?nocache=true'

        # View item page in future
        with mock.patch('aristotle_mdr.utils.utils.timezone.now') as mock_now:
            mock_now.return_value = self.future_time

            self.login_editor()

            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertNotEqual(response.content, b'wow')

    @tag('cache')
    @override_settings(CACHE_ITEM_PAGE=True)
    @skip('Cache mixin not currently used')
    def test_itempage_cached_per_user(self):
        # Load response into cache
        cache.set(self.cache_key, HttpResponse('wow'))

        # View item page in future
        with mock.patch('aristotle_mdr.utils.utils.timezone.now') as mock_now:
            mock_now.return_value = self.future_time

            # Login as different user
            self.login_viewer()
            response = self.reverse_get(
                'aristotle:item',
                reverse_args=[self.itemid, 'objectclass', 'test-item'],
                status_code=200
            )

            self.assertNotEqual(response.content, b'wow')

    @tag('cache')
    @override_settings(CACHE_ITEM_PAGE=False)
    @skip('Cache mixin not currently used')
    def test_itempage_not_loaded_from_cache_if_setting_false(self):
        # Load response into cache
        cache.set(self.cache_key, HttpResponse('wow'))

        # View item page in future
        with mock.patch('aristotle_mdr.utils.utils.timezone.now') as mock_now:
            mock_now.return_value = self.future_time

            # Login as different user
            self.login_editor()
            response = self.reverse_get(
                'aristotle:item',
                reverse_args=[self.itemid, 'objectclass', 'test-item'],
                status_code=200
            )

            self.assertNotEqual(response.content, b'wow')

    @tag('cache')
    @override_settings(CACHE_ITEM_PAGE=False)
    @skip('Cache mixin not currently used')
    def test_response_not_put_into_cache_if_setting_false(self):
        # View in the future to avoid modified recently check
        with mock.patch('aristotle_mdr.utils.utils.timezone.now') as mock_now:
            mock_now.return_value = self.future_time

            self.login_editor()
            response = self.reverse_get(
                'aristotle:item',
                reverse_args=[self.itemid, 'objectclass', 'test-item'],
                status_code=200
            )

        cached_itempage = cache.get(self.cache_key, None)
        self.assertIsNone(cached_itempage)

    @tag('extrav')
    def test_no_extra_versions_created_in_advanced_editor(self):
        oc = MDR.ObjectClass.objects.create(
            name='Test OC',
            definition='Just a test',
            submitter=self.editor
        )

        prop = MDR.Property.objects.create(
            name='Test Prop',
            definition='Just a test',
            submitter=self.editor
        )

        data_element_concept = MDR.DataElementConcept.objects.create(
            name='Test DEC',
            definition='Just a test',
            objectClass=oc,
            property=prop,
            submitter=self.editor
        )

        data = utils.model_to_dict_with_change_time(data_element_concept)
        data.update({
            'definition': 'More than a test',
            'change_comments': 'A change was made'
        })

        self.assertEqual(revmodels.Version.objects.count(), 0)

        self.login_editor()
        response = self.reverse_post(
            'aristotle:edit_item',
            data=data,
            status_code=302,
            reverse_args=[data_element_concept.id]
        )

        data_element_concept = MDR.DataElementConcept.objects.get(pk=data_element_concept.pk)
        self.assertEqual(data_element_concept.definition, 'More than a test')

        # There is only one version being saved right now, on the item
        self.assertEqual(revmodels.Version.objects.count(), 1)

        dec_ct = ContentType.objects.get_for_model(MDR.DataElementConcept)

        dec_version = revmodels.Version.objects.get(content_type=dec_ct)

        # check dec version
        self.assertEqual(int(dec_version.object_id), data_element_concept.id)

    @tag('version')
    def test_display_version_concept_info(self):
        self.item.references = '<p>refs</p>'

        with reversion.create_revision():
            self.item.save()

        latest = reversion.models.Version.objects.get_for_object(self.item).first()

        self.login_editor()
        response = self.reverse_get(
            'aristotle:item_version',
            reverse_args=[latest.id],
            status_code=200
        )

        fields = {f.heading: f for f in response.context['item']['item_fields']}
        self.assertTrue('References' in fields)
        references = fields['References']
        self.assertFalse(references.is_link)
        self.assertTrue(references.is_html)
        self.assertEqual(references.value, '<p>refs</p>')

    @tag('version')
    def test_version_display_custom_value_html(self):
        field = CustomField.objects.create(
            order=0,
            name='Some random html',
            type='html',
        )
        value = CustomValue.objects.create(
            field=field,
            concept=self.item.concept,
            content='<p>This is html</p>'
        )

        self.assertGreater(self.item.concept.customvalue_set.all().count(), 0)

        with reversion.create_revision():
            self.item.save()
        latest = reversion.models.Version.objects.get_for_object(self.item).first()

        self.login_editor()
        response = self.reverse_get(
            'aristotle:item_version',
            reverse_args=[latest.id],
            status_code=200
        )

        fields = {f.heading: f for f in response.context['item']['item_fields']}
        cv_field = fields['Custom Values']
        self.assertGreater(len(cv_field.sub_fields), 0)

        first_cv = {f.heading: f for f in cv_field.sub_fields[0]}
        self.assertEqual(first_cv['Custom Field'].obj, field)
        self.assertTrue(first_cv['Content'].is_html)

    def test_display_item_histroy_without_wg(self):
        self.item.workgroup = None
        with reversion.create_revision():
            self.item.save()

        self.login_superuser()
        response = self.reverse_get(
            'aristotle:item_history',
            reverse_args=[self.item.id],
        )
        self.assertEqual(response.status_code, 200)

    @tag('item_app_check')
    def test_viewing_item_with_disabled_app(self):
        enabled_apps = ['aristotle_dse']
        with mock.patch('aristotle_mdr.views.views.fetch_metadata_apps', return_value=enabled_apps):
            self.login_editor()
            self.reverse_get(
                'aristotle:item',
                reverse_args=[self.item.id, 'objectclass', 'name'],
                status_code=404
            )

    @tag('item_app_check')
    def test_viewing_item_with_enabled_app(self):
        enabled_apps = ['aristotle_mdr']
        with mock.patch('aristotle_mdr.views.views.fetch_metadata_apps', return_value=enabled_apps):
            self.login_editor()
            self.reverse_get(
                'aristotle:item',
                reverse_args=[self.item.id, 'objectclass', 'name'],
                status_code=200
            )

    @tag('version')
    def test_version_workgroup_lookup(self):
        with reversion.create_revision():
            self.item.save()

        latest = reversion.models.Version.objects.get_for_object(self.item).first()

        self.login_viewer()
        response = self.reverse_get(
            'aristotle:item_version',
            reverse_args=[latest.id],
            status_code=200
        )

        workgroup = response.context['item']['workgroup']
        self.assertEqual(workgroup, self.wg1)

    @tag('version')
    def test_version_item_metadata(self):
        # Does this make it meta meta data?

        with reversion.create_revision():
            self.item.save()

        latest = reversion.models.Version.objects.get_for_object(self.item).first()

        self.login_viewer()
        response = self.reverse_get(
            'aristotle:item_version',
            reverse_args=[latest.id],
            status_code=200
        )

        idstr = str(self.item.id)
        self.assertEqual(response.context['item']['id'], idstr)
        self.assertEqual(response.context['item']['pk'], idstr)
        self.assertEqual(response.context['item']['meta']['app_label'], 'aristotle_mdr')
        self.assertEqual(response.context['item']['meta']['model_name'], 'objectclass')
        self.assertEqual(response.context['item']['get_verbose_name'], 'Object Class')

    @tag('version')
    def test_view_non_concept_version(self):
        with reversion.create_revision():
            self.wg1.save()

        latest = reversion.models.Version.objects.get_for_object(self.wg1).first()

        self.login_viewer()
        response = self.reverse_get(
            'aristotle:item_version',
            reverse_args=[latest.id],
            status_code=404
        )

    @tag('version')
    def test_view_version_for_item_without_perm(self):
        with reversion.create_revision():
            item = MDR.ObjectClass.objects.create(
                name='cant view',
                definition='cant see this one',
                submitter=self.editor
            )

        latest = reversion.models.Version.objects.get_for_object(item).first()

        self.login_viewer()
        response = self.reverse_get(
            'aristotle:item_version',
            reverse_args=[latest.id],
            status_code=403
        )

    @tag('custfield')
    def test_submitter_can_save_via_edit_page_with_custom_fields(self):
        self.login_editor()
        cf = CustomField.objects.create(
            name='MyCustomField',
            type='int',
            help_text='Custom',
            order=0
        )
        postdata = utils.model_to_dict_with_change_time(self.item)
        postdata[cf.form_field_name] = 4
        response = self.reverse_post(
            'aristotle:edit_item',
            postdata,
            reverse_args=[self.item.id],
            status_code=302
        )
        self.item1 = MDR.ObjectClass.objects.get(pk=self.item.pk)
        self.assertRedirects(response, url_slugify_concept(self.item))

        cv_query = CustomValue.objects.filter(
            field=cf,
            concept=self.item1._concept_ptr
        )
        self.assertTrue(cv_query.count(), 1)
        cv = cv_query.first()
        self.assertEqual(cv.content, '4')

    @tag('custfield')
    def test_edit_page_custom_fields_initial(self):
        self.login_editor()
        cf = CustomField.objects.create(
            name='MyCustomField',
            type='int',
            help_text='Custom',
            order=0
        )
        cv = CustomValue.objects.create(
            field=cf,
            concept=self.item,
            content='4'
        )
        response = self.reverse_get(
            'aristotle:edit_item',
            reverse_args=[self.item.id],
            status_code=200
        )
        initial = response.context['form'].initial
        self.assertTrue(cf.form_field_name in initial)
        self.assertEqual(initial[cf.form_field_name], '4')

    @tag('custfield')
    def test_edit_page_custom_field_non_enum_initial(self):
        """Test handling of initial value not in emum list"""
        self.login_editor()
        # Add field and value
        cf = CustomField.objects.create(
            name='Pokemon',
            type='enum',
            help_text='Custom',
            choices='Charmander,Squirtle',
            order=0
        )
        cv = CustomValue.objects.create(
            field=cf,
            concept=self.item,
            content='Bulbasaur'
        )
        # Edit item
        response = self.reverse_get(
            'aristotle:edit_item',
            reverse_args=[self.item.id],
            status_code=200
        )
        # Check in initial
        form = response.context['form']
        self.assertTrue(cf.form_field_name in form.initial)
        self.assertEqual(form.initial[cf.form_field_name], 'Bulbasaur')
        field = form.fields['custom_Pokemon_{}'.format(cf.id)]
        # Make sure bad value was added as last option
        self.assertEqual(field.choices[-1][0], 'Bulbasaur')

    def get_custom_values_for_user(self, user):
        """Util function used for the following 3 tests"""
        view = ConceptRenderView()
        request = self.factory.get('/anitemurl/')
        request.user = user
        view.request = request
        view.item = self.item
        return view.get_custom_values()

    @tag('custfield')
    def test_view_custom_values_unath(self):
        self.setup_custom_values()
        anon = AnonymousUser()
        cvs = self.get_custom_values_for_user(anon)
        self.assertEqual(len(cvs), 1)
        self.assertEqual(cvs[0].content, 'All Value')

    @tag('custfield')
    def test_view_custom_values_auth(self):
        self.setup_custom_values()
        cvs = self.get_custom_values_for_user(self.regular)
        self.assertEqual(len(cvs), 2)
        self.assertEqual(cvs[0].content, 'All Value')
        self.assertEqual(cvs[1].content, 'Auth Value')

    @tag('custfield')
    def test_view_custom_values_auth(self):
        self.setup_custom_values()
        cvs = self.get_custom_values_for_user(self.viewer)
        self.assertEqual(len(cvs), 3)
        self.assertEqual(cvs[0].content, 'All Value')
        self.assertEqual(cvs[1].content, 'Auth Value')
        self.assertEqual(cvs[2].content, 'Workgroup Value')

    @tag('nonwg')
    def test_add_wg_to_non_wg_item(self):
        self.item.workgroup = None
        self.item.save()

        updated_item = utils.model_to_dict_with_change_time(self.item)
        updated_item['workgroup'] = str(self.wg1.id)

        self.login_editor()
        response = self.client.post(
            reverse('aristotle:edit_item', args=[self.item.id]),
            updated_item
        )
        self.assertEqual(response.status_code, 302)
        updated = MDR.ObjectClass.objects.get(id=self.item.id)
        self.assertEqual(updated.workgroup, self.wg1)

    def test_user_cannot_add_item_to_workgroup_they_are_not_member_of(self):
        """Tests that a user cannot add an item to a workgroup they are not a member of"""
        # Create some items
        other_workgroup = MDR.Workgroup.objects.create(name="The other workgroup",
                                                       stewardship_organisation=self.steward_org_1
                                                       )
        reggies_workgroup = MDR.Workgroup.objects.create(name="Reggie's Workgroup",
                                                         stewardship_organisation=self.steward_org_1)

        object_class = MDR.ObjectClass.objects.create(name='Object Class',
                                                      definition="This is a new and important object class",
                                                      workgroup=reggies_workgroup)
        reggie = get_user_model().objects.create_user('reggie_regular@example.com',
                                                      'verySecurePassword')
        reggies_workgroup.giveRoleToUser('manager', reggie)
        response = self.client.post(reverse('friendly_login'), {'username': 'reggie_regular@example.com',
                                                                'password': 'verySecurePassword'})
        self.assertEqual(response.status_code, 302)

        # Check that Reggie cannot add his item to a workgroup he is not a member of
        response = self.client.get(reverse('aristotle:edit_item', args=[object_class.pk]))
        self.assertResponseStatusCodeEqual(response=response, code=200)

        updated_item = utils.model_to_dict_with_change_time(object_class)
        updated_item['workgroup'] = str(other_workgroup.id)
        response = self.client.post(
            reverse('aristotle:edit_item', args=[object_class.id]),
            updated_item
        )
        self.assertResponseStatusCodeEqual(response=response, code=200)
        self.assertEqual(object_class.workgroup, reggies_workgroup)


    def test_non_existent_item_404(self):
        response = self.reverse_get(
            'aristotle:item',
            reverse_args=[55555]
        )
        self.assertEqual(response.status_code, 404)

    def test_history_compare_with_bad_version_data(self):
        """ Test that if the version compare view is passed garbled serialized data that the view does not attempt
        to load it  """
        versions = self.create_versions()

        first_version = versions.first()

        # Mangle the last version's serialized data
        last_version = versions.order_by('-revision__date_created').first()
        last_version.serialized_data = '{"""}{,,}}}}'
        last_version.save()

        # Look at the particular view
        qparams = '?v1={}&v2={}'.format(first_version.id, last_version.id)
        self.login_editor()
        response = self.client.get(
            reverse('aristotle:compare_versions', args=[self.item.id]) + qparams
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['cannot_compare'])
        self.assertContains(response, 'Those versions could not be compared')

    def test_view_item_version_with_bad_data(self):
        versions = self.create_versions()
        # Mangle the last versions serialized data
        last_version = versions.order_by('-revision__date_created').first()
        last_version.serialized_data = '{"""}{,,}}}}'
        last_version.save()

        self.login_editor()
        response = self.client.get(
            reverse('aristotle:item_version', args=[last_version.id])
        )
        self.assertEqual(response.status_code, 404)

    def test_comparator_with_bad_version_data(self):
        """Test that the comparator still works with garbled version data"""
        versions = self.create_versions()
        # Mangle the last versions serialized data
        last_version = versions.order_by('-revision__date_created').first()
        last_version.serialized_data = '(V)(;,,;)(V)'  # Need an error, why not Zoidberg?
        last_version.save()

        # Create second item for compare
        with reversion.create_revision():
            item2 = MDR.ObjectClass.objects.create(
                name='Second',
                definition='Second',
                submitter=self.editor
            )
        qparams = '?item_a={}&item_b={}'.format(self.item.id, item2.id)

        self.login_editor()
        response = self.client.get(
            reverse('aristotle:compare_concepts') + qparams
        )
        self.assertEqual(response.status_code, 200)
        # Check that the cannot compare is set by bad version data, and that the page loads
        self.assertEqual(response.context['cannot_compare'], True)


class LoggedInViewConceptPages(utils.AristotleTestUtils):
    """These are run by all item types"""
    defaults = {}

    def setUp(self):
        super().setUp()

        self.item1 = self.itemType.objects.create(
            name="Test Item 1 (visible to tested viewers)",
            definition="my definition",
            workgroup=self.wg1,
            **self.defaults
        )
        self.item2 = self.itemType.objects.create(
            name="Test Item 2 (NOT visible to tested viewers)",
            definition="my definition",
            workgroup=self.wg2,
            **self.defaults
        )
        self.item3 = self.itemType.objects.create(
            name="Test Item 3 (visible to tested viewers)",
            definition="my definition",
            workgroup=self.wg1,
            **self.defaults
        )
        self.steward_org = MDR.StewardOrganisation.objects.create(name="Test SO")

    def load_help(self):
        from django.core.management import call_command
        call_command('load_aristotle_help', verbosity=0)

    def update_definition_with_versions(self, new_defn='brand new definition'):
        with reversion.create_revision():
            self.item1.save()

        with reversion.create_revision():
            self.item1.definition = new_defn
            self.item1.save()

        item1_concept = self.item1.item

        concept_versions = reversion.models.Version.objects.get_for_object(item1_concept)
        self.assertEqual(concept_versions.count(), 2)

        item_versions = reversion.models.Version.objects.get_for_object(self.item1)
        self.assertEqual(item_versions.count(), 2)

    def change_status(self, item, user, ra, cascade=False):
        self.make_review_request(item, user)

        response = self.client.get(reverse('aristotle:changeStatus', args=[item.id]))
        self.assertEqual(response.status_code, 200)

        cascade_post = 0
        if cascade:
            cascade_post = 1

        response = self.client.post(
            reverse('aristotle:changeStatus', args=[item.id]),
            {
                'change_status-registrationAuthorities': [str(ra.id)],
                'change_status-state': ra.public_state,
                'change_status-changeDetails': "testing",
                'change_status-cascadeRegistration': cascade_post,
                'submit_skip': 'value',
                'change_status_view-current_step': 'change_status',
            }
        )
        self.assertRedirects(response, url_slugify_concept(item))


    def test_su_can_view(self):
        self.login_superuser()
        response = self.client.get(self.get_page(self.item1))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(self.get_page(self.item2))
        self.assertEqual(response.status_code, 200)

        # Ensure short urls redirect properly
        response = self.client.get(reverse("aristotle:item_short", args=[self.item1.pk]))
        self.assertEqual(response.status_code, 302)

    def test_editor_can_view(self):
        self.login_editor()
        response = self.client.get(self.get_page(self.item1))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(self.get_page(self.item2))
        self.assertEqual(response.status_code, 403)

    def test_viewer_can_view(self):
        self.login_viewer()
        response = self.client.get(self.get_page(self.item1))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(self.get_page(self.item2))
        self.assertEqual(response.status_code, 403)

    def test_stubs_redirect_correctly(self):
        self.login_viewer()
        response = self.client.get(reverse('aristotle:item', args=[self.item1.id]))
        self.assertRedirects(response, url_slugify_concept(self.item1))
        response = self.client.get(reverse('aristotle:item', args=[self.item1.id]) + "/not-a-model/fake-name")
        self.assertRedirects(response, url_slugify_concept(self.item1))
        response = self.client.get(reverse('aristotle:item', args=[self.item1.id]) + "/this-isnt-even-a-proper-stub")
        self.assertRedirects(response, url_slugify_concept(self.item1))

    def test_uuids_redirect_correctly(self):
        self.login_viewer()
        response = self.client.get(reverse('aristotle:item_uuid', args=[self.item1.uuid]))
        self.assertRedirects(response, url_slugify_concept(self.item1))

    def test_anon_cannot_view_edit_page(self):
        self.logout()
        response = self.client.get(reverse('aristotle:edit_item', args=[self.item1.id]))
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('aristotle:edit_item', args=[self.item2.id]))
        self.assertEqual(response.status_code, 302)

    def test_viewer_cannot_view_edit_page(self):
        self.login_viewer()
        response = self.client.get(reverse('aristotle:edit_item', args=[self.item1.id]))
        self.assertEqual(response.status_code, 403)
        response = self.client.get(reverse('aristotle:edit_item', args=[self.item2.id]))
        self.assertEqual(response.status_code, 403)

    def test_submitter_can_view_edit_page(self):
        self.login_editor()
        response = self.client.get(reverse('aristotle:edit_item', args=[self.item1.id]))
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue('change_comments' in form.fields)

        response = self.client.get(reverse('aristotle:edit_item', args=[self.item2.id]))
        self.assertEqual(response.status_code, 403)

    def test_regular_can_view_own_items_edit_page(self):
        self.login_regular_user()
        response = self.client.get(reverse('aristotle:edit_item', args=[self.item1.id]))
        self.assertEqual(response.status_code, 403)
        response = self.client.get(reverse('aristotle:edit_item', args=[self.item2.id]))
        self.assertEqual(response.status_code, 403)
        self.regular_item = self.itemType.objects.create(name="regular item", definition="my definition",
                                                         submitter=self.regular, **self.defaults)
        response = self.client.get(reverse('aristotle:edit_item', args=[self.regular_item.id]))
        self.assertEqual(response.status_code, 200)

    def test_regular_can_save_via_edit_page(self):
        self.login_regular_user()
        self.regular_item = self.itemType.objects.create(name="regular item", definition="my definition",
                                                         submitter=self.regular, **self.defaults)
        response = self.client.get(reverse('aristotle:edit_item', args=[self.regular_item.id]))
        self.assertEqual(response.status_code, 200)

        updated_item = utils.model_to_dict_with_change_time(response.context['item'])
        updated_name = updated_item['name'] + " updated!"
        updated_item['name'] = updated_name
        response = self.client.post(reverse('aristotle:edit_item', args=[self.regular_item.id]), updated_item)
        self.regular_item = self.itemType.objects.get(pk=self.regular_item.pk)
        self.assertRedirects(response, url_slugify_concept(self.regular_item))
        self.assertEqual(self.regular_item.name, updated_name)

    def test_submitter_can_save_via_edit_page(self):
        self.login_editor()
        response = self.client.get(reverse('aristotle:edit_item', args=[self.item1.id]))
        self.assertEqual(response.status_code, 200)

        updated_item = utils.model_to_dict_with_change_time(response.context['item'])
        updated_name = updated_item['name'] + " updated!"
        updated_item['name'] = updated_name

        response = self.client.post(reverse('aristotle:edit_item', args=[self.item1.id]), updated_item)
        self.item1 = self.itemType.objects.get(pk=self.item1.pk)
        self.assertRedirects(response, url_slugify_concept(self.item1))
        self.assertEqual(self.item1.name, updated_name)

    def test_submitter_can_save_item_with_no_workgroup_via_edit_page(self):
        self.login_editor()
        self.item1 = self.itemType.objects.create(name="Test Item 1 (visible to tested viewers)", submitter=self.editor,
                                                  definition="my definition", **self.defaults)
        response = self.client.get(reverse('aristotle:edit_item', args=[self.item1.id]))
        self.assertEqual(response.status_code, 200)

        updated_item = utils.model_to_dict_with_change_time(response.context['item'])
        updated_name = updated_item['name'] + " updated!"
        updated_item['name'] = updated_name
        response = self.client.post(reverse('aristotle:edit_item', args=[self.item1.id]), updated_item)
        self.item1 = self.itemType.objects.get(pk=self.item1.pk)
        self.assertRedirects(response, url_slugify_concept(self.item1))
        self.assertEqual(self.item1.name, updated_name)
        self.assertEqual(self.item1.workgroup, None)

    def test_submitter_can_save_via_edit_page_with_change_comment(self):
        self.login_editor()
        response = self.client.get(reverse('aristotle:edit_item', args=[self.item1.id]))
        self.assertEqual(response.status_code, 200)

        # Edit the item
        updated_item = utils.model_to_dict_with_change_time(response.context['item'])
        updated_name = updated_item['name'] + " updated!"
        updated_item['name'] = updated_name
        change_comment = "I changed this because I can"
        updated_item['change_comments'] = change_comment
        response = self.client.post(reverse('aristotle:edit_item', args=[self.item1.id]), updated_item)
        self.item1 = self.itemType.objects.get(pk=self.item1.pk)

        self.assertRedirects(response, url_slugify_concept(self.item1))
        self.assertEqual(self.item1.name, updated_name)

        # Assert that the change comment is displayed
        response = self.client.get(reverse('aristotle:item_history', args=[self.item1.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, change_comment)

        # Logout, and assert that the page is not displayed
        self.logout()
        response = self.client.get(reverse('aristotle:item_history', args=[self.item1.id]))
        self.assertEqual(response.status_code, 403)

        MDR.Status.objects.create(
            concept=self.item1,
            registrationAuthority=self.ra,
            registrationDate=datetime.date(2009, 4, 28),
            state=MDR.STATES.standard
        )

        self.item1 = self.itemType.objects.get(pk=self.item1.pk)
        self.assertTrue(self.item1._is_public)
        self.assertTrue(self.item1.can_view(None))

        response = self.client.get(self.get_page(self.item1))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('aristotle:item_history', args=[self.item1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, change_comment)

    def test_submitter_can_save_via_edit_page_with_slots(self):
        self.login_editor()
        response = self.client.get(reverse('aristotle:edit_item', args=[self.item1.id]))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(self.item1.slots.count(), 0)

        updated_item = utils.model_to_dict_with_change_time(response.context['item'])
        updated_name = updated_item['name'] + " updated!"
        updated_item['name'] = updated_name

        formset_data = [
            {
                'concept': self.item1.pk,
                'name': 'extra',
                'type': 'string',
                'value': 'test slot value',
                'order': 0,
                'permission': 0,
            },
            {
                'concept': self.item1.pk,
                'name': 'more_extra',
                'type': 'string',
                'value': 'an even better test slot value',
                'order': 1,
                'permission': 0,
            }
        ]
        slot_formset_data = self.get_formset_postdata(formset_data, 'slots')

        updated_item.update(slot_formset_data)

        response = self.client.post(reverse('aristotle:edit_item', args=[self.item1.id]), updated_item)
        self.item1 = self.itemType.objects.get(pk=self.item1.pk)

        self.assertRedirects(response, url_slugify_concept(self.item1))
        self.assertEqual(self.item1.slots.count(), 2)

        response = self.client.get(reverse('aristotle:edit_item', args=[self.item1.id]))
        self.assertContains(response, 'test slot value')
        self.assertContains(response, 'an even better test slot value')

        slots = self.item1.slots.all()
        self.assertEqual(slots[0].name, 'extra')
        self.assertEqual(slots[0].order, 0)
        self.assertEqual(slots[1].name, 'more_extra')
        self.assertEqual(slots[1].order, 1)

    def test_submitter_can_save_via_edit_page_with_identifiers(self):

        self.login_editor()
        response = self.client.get(reverse('aristotle:edit_item', args=[self.item1.id]))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(self.item1.slots.count(), 0)

        updated_item = utils.model_to_dict_with_change_time(response.context['item'])
        updated_name = updated_item['name'] + " updated!"
        updated_item['name'] = updated_name

        namespace = ident_models.Namespace.objects.create(
            stewardship_organisation=self.steward_org,
            shorthand_prefix='pre'
        )

        formset_data = [
            {
                'concept': self.item1.pk,
                'namespace': namespace.pk,
                'identifier': 'YE',
                'version': 1,
                'order': 0
            },
            {
                'concept': self.item1.pk,
                'namespace': namespace.pk,
                'identifier': 'RE',
                'version': 1,
                'order': 1
            }
        ]
        ident_formset_data = self.get_formset_postdata(formset_data, 'identifiers')

        updated_item.update(ident_formset_data)

        response = self.client.post(reverse('aristotle:edit_item', args=[self.item1.id]), updated_item)
        self.item1 = self.itemType.objects.get(pk=self.item1.pk)

        self.assertRedirects(response, url_slugify_concept(self.item1))
        self.assertEqual(self.item1.identifiers.count(), 2)

        response = self.client.get(reverse('aristotle:item', args=[self.item1.id]), follow=True)
        self.assertContains(response, 'pre</a>/YE/1')
        self.assertContains(response, 'pre</a>/RE/1')

        idents = self.item1.identifiers.all()
        self.assertEqual(idents[0].identifier, 'YE')
        self.assertEqual(idents[0].order, 0)
        self.assertEqual(idents[1].identifier, 'RE')
        self.assertEqual(idents[1].order, 1)

    def test_submitter_cannot_save_via_edit_page_if_other_saves_made(self):

        self.login_editor()
        modified = self.item1.modified
        response = self.client.get(reverse('aristotle:edit_item', args=[self.item1.id]))
        self.assertEqual(response.status_code, 200)

        # fake that we fetched the page seconds before modification
        updated_item = utils.model_to_dict_with_change_time(response.context['item'],
                                                            fetch_time=modified - datetime.timedelta(seconds=5))
        updated_name = updated_item['name'] + " updated!"
        updated_item['name'] = updated_name
        change_comment = "I changed this because I can"
        updated_item['change_comments'] = change_comment
        time_before_response = timezone.now()
        response = self.client.post(reverse('aristotle:edit_item', args=[self.item1.id]), updated_item)

        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(form.errors['last_fetched'][0] == CheckIfModifiedMixin.modified_since_form_fetched_error)

        # When sending a response with a bad last_fetch, the new one should come back right
        self.assertTrue(time_before_response < form.fields['last_fetched'].initial)

        # With the new last_fetched we can submit ok!
        updated_item['last_fetched'] = form.fields['last_fetched'].initial
        response = self.client.post(reverse('aristotle:edit_item', args=[self.item1.id]), updated_item)
        self.assertEqual(response.status_code, 302)

        updated_item.pop('last_fetched')
        time_before_response = timezone.now()
        response = self.client.post(reverse('aristotle:edit_item', args=[self.item1.id]), updated_item)

        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(form.errors['last_fetched'][0] == CheckIfModifiedMixin.modified_since_field_missing)
        # When sending a response with no last_fetch, the new one should come back right
        self.assertTrue(time_before_response < form.fields['last_fetched'].initial)

        # With the new last_fetched we can submit ok!
        updated_item['last_fetched'] = form.fields['last_fetched'].initial
        response = self.client.post(reverse('aristotle:edit_item', args=[self.item1.id]), updated_item)
        self.assertEqual(response.status_code, 302)

    # Test if workgroup-moving settings work

    @override_settings(ARISTOTLE_SETTINGS=dict(settings.ARISTOTLE_SETTINGS, WORKGROUP_CHANGES=[]))
    def test_submitter_cannot_change_workgroup_via_edit_page(self):
        # based on the idea that 'submitter' is not set in ARISTOTLE_SETTINGS.WORKGROUP
        self.wg_other = MDR.Workgroup.objects.create(name="Test WG to move to",
                                                     stewardship_organisation=self.steward_org)
        self.wg_other.giveRoleToUser('submitter', self.editor)

        self.login_editor()
        response = self.client.get(reverse('aristotle:edit_item', args=[self.item1.id]))
        self.assertEqual(response.status_code, 200)

        updated_item = utils.model_to_dict_with_change_time(response.context['item'])

        updated_item['workgroup'] = str(self.wg_other.pk)

        response = self.client.post(reverse('aristotle:edit_item', args=[self.item1.id]), updated_item)
        self.assertEqual(response.status_code, 200)

        form = response.context['form']

        self.assertTrue('workgroup' in form.errors.keys())
        self.assertTrue(len(form.errors['workgroup']) == 1)

        # Submitter is logged in, tries to move item - fails because
        self.assertFalse(perms.user_can_remove_from_workgroup(self.editor, self.item1.workgroup))
        self.assertTrue(form.errors['workgroup'][0] == WorkgroupVerificationMixin.cant_move_from_permission_error)

        updated_item['workgroup'] = str(self.wg2.pk)
        response = self.client.post(reverse('aristotle:edit_item', args=[self.item1.id]), updated_item)
        self.assertEqual(response.status_code, 200)

        form = response.context['form']

        self.assertTrue('workgroup' in form.errors.keys())
        self.assertTrue(len(form.errors['workgroup']) == 1)

        self.assertTrue('Select a valid choice.' in form.errors['workgroup'][0])

    @override_settings(ARISTOTLE_SETTINGS=dict(settings.ARISTOTLE_SETTINGS, WORKGROUP_CHANGES=['submitter']))
    def test_submitter_can_change_workgroup_via_edit_page(self):
        # based on the idea that 'submitter' is set in ARISTOTLE_SETTINGS.WORKGROUP
        self.wg_other = MDR.Workgroup.objects.create(name="Test WG to move to",
                                                     stewardship_organisation=self.steward_org)

        self.login_editor()
        response = self.client.get(reverse('aristotle:edit_item', args=[self.item1.id]))
        self.assertEqual(response.status_code, 200)
        updated_item = utils.model_to_dict_with_change_time(response.context['item'])
        updated_item['workgroup'] = str(self.wg_other.pk)

        response = self.client.post(reverse('aristotle:edit_item', args=[self.item1.id]), updated_item)
        self.assertEqual(response.status_code, 200)

        form = response.context['form']

        self.assertTrue('Select a valid choice.' in form.errors['workgroup'][0])

        self.wg_other.giveRoleToUser('submitter', self.editor)

        response = self.client.get(reverse('aristotle:edit_item', args=[self.item1.id]))
        response = self.client.post(reverse('aristotle:edit_item', args=[self.item1.id]), updated_item)

        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('aristotle:edit_item', args=[self.item1.id]))
        updated_item = utils.model_to_dict_with_change_time(response.context['item'])
        updated_item['workgroup'] = str(self.wg2.pk)
        response = self.client.post(reverse('aristotle:edit_item', args=[self.item1.id]), updated_item)
        self.assertEqual(response.status_code, 200)

        self.assertTrue('Select a valid choice.' in form.errors['workgroup'][0])

    @override_settings(ARISTOTLE_SETTINGS=dict(settings.ARISTOTLE_SETTINGS, WORKGROUP_CHANGES=['admin']))
    def test_admin_can_change_workgroup_via_edit_page(self):
        # based on the idea that 'admin' is set in ARISTOTLE_SETTINGS.WORKGROUP
        self.wg_other = MDR.Workgroup.objects.create(name="Test WG to move to",
                                                     stewardship_organisation=self.steward_org)

        self.login_superuser()
        response = self.client.get(reverse('aristotle:edit_item', args=[self.item1.id]))
        self.assertEqual(response.status_code, 200)
        updated_item = utils.model_to_dict_with_change_time(self.item1)
        updated_item['workgroup'] = str(self.wg_other.pk)

        response = self.client.post(reverse('aristotle:edit_item', args=[self.item1.id]), updated_item)
        self.assertEqual(response.status_code, 302)

        updated_item = utils.model_to_dict_with_change_time(self.item1)
        updated_item['workgroup'] = str(self.wg2.pk)
        response = self.client.post(reverse('aristotle:edit_item', args=[self.item1.id]), updated_item)
        self.assertEqual(response.status_code, 302)

    @override_settings(ARISTOTLE_SETTINGS=dict(settings.ARISTOTLE_SETTINGS, WORKGROUP_CHANGES=['manager']))
    def test_manager_of_two_workgroups_can_change_workgroup_via_edit_page(self):
        # based on the idea that 'manager' is set in ARISTOTLE_SETTINGS.WORKGROUP
        self.wg_other = MDR.Workgroup.objects.create(name="Test WG to move to",
                                                     stewardship_organisation=self.steward_org)
        self.wg_other.giveRoleToUser('submitter', self.editor)

        self.login_editor()
        response = self.client.get(reverse('aristotle:edit_item', args=[self.item1.id]))
        self.assertEqual(response.status_code, 200)
        updated_item = utils.model_to_dict_with_change_time(response.context['item'])
        updated_item['workgroup'] = str(self.wg_other.pk)
        response = self.client.post(reverse('aristotle:edit_item', args=[self.item1.id]), updated_item)
        self.assertEqual(response.status_code, 200)

        form = response.context['form']
        # Submitter can't move because they aren't a manager of any workgroups.
        self.assertTrue(form.errors['workgroup'][0] == WorkgroupVerificationMixin.cant_move_from_permission_error)

        self.wg1.giveRoleToUser('manager', self.editor)

        response = self.client.post(reverse('aristotle:edit_item', args=[self.item1.id]), updated_item)
        self.assertEqual(response.status_code, 200)

        form = response.context['form']
        # Submitter can't move because they aren't a manager of the workgroup the item is in.
        self.assertTrue(form.errors['workgroup'][0] == WorkgroupVerificationMixin.cant_move_to_permission_error)

        self.login_manager()

        response = self.client.post(reverse('aristotle:edit_item', args=[self.item1.id]), updated_item)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']

        self.assertTrue('Select a valid choice.' in form.errors['workgroup'][0])

        self.wg_other.giveRoleToUser('manager', self.manager)

        response = self.client.post(reverse('aristotle:edit_item', args=[self.item1.id]), updated_item)
        self.assertEqual(response.status_code, 302)

        updated_item['workgroup'] = str(self.wg2.pk)
        response = self.client.post(reverse('aristotle:edit_item', args=[self.item1.id]), updated_item)
        self.assertEqual(response.status_code, 200)

        self.assertTrue('Select a valid choice.' in form.errors['workgroup'][0])

    @tag('clone_item')
    def test_anon_cannot_view_clone_page(self):
        self.logout()
        response = self.client.get(reverse('aristotle:clone_item', args=[self.item1.id]))
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('aristotle:clone_item', args=[self.item2.id]))
        self.assertEqual(response.status_code, 302)

    @tag('clone_item')
    def test_viewer_can_view_clone_page(self):
        self.login_viewer()
        # Viewer can clone an item they can see
        self.assertTrue(perms.user_can_view(self.viewer, self.item1))
        response = self.client.get(reverse('aristotle:clone_item', args=[self.item1.id]))
        self.assertEqual(response.status_code, 200)

        # Viewer can't clone an item they can't see
        self.assertFalse(perms.user_can_view(self.viewer, self.item2))
        response = self.client.get(reverse('aristotle:clone_item', args=[self.item2.id]))
        self.assertEqual(response.status_code, 403)

    @tag('clone_item')
    def test_submitter_can_view_clone_page(self):
        self.login_editor()
        response = self.client.get(reverse('aristotle:clone_item', args=[self.item1.id]))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('aristotle:clone_item', args=[self.item2.id]))
        self.assertEqual(response.status_code, 403)

    @tag('clone_item')
    def test_submitter_can_save_via_clone_page(self):
        self.login_editor()

        import time
        time.sleep(2)  # Delay so there is a time difference between original item and new item
        response = self.client.get(reverse('aristotle:clone_item', args=[self.item1.id]))
        self.assertEqual(response.status_code, 200)

        updated_item = self.get_updated_data_for_clone(response)
        updated_name = updated_item['name'] + " cloned!"
        updated_item['name'] = updated_name
        updated_item.update(utils.get_management_forms(self.item1, identifiers=True, slots=True))

        response = self.client.post(reverse('aristotle:clone_item', args=[self.item1.id]), updated_item)
        most_recent = response.context[-1]['object']  # Get the item back to check

        self.assertTrue(perms.user_can_view(self.editor, most_recent))
        self.assertRedirects(response, url_slugify_concept(most_recent))
        self.assertEqual(most_recent.name, updated_name)

        # Make sure the right item was save and our original hasn't been altered
        self.item1 = self.itemType.objects.get(id=self.item1.id)  # Refresh from cache
        self.assertTrue('cloned' not in self.item1.name)

    @tag('clone_item')
    def test_submitter_can_save_via_clone_page_with_no_workgroup(self):
        self.login_editor()
        response = self.client.get(reverse('aristotle:clone_item', args=[self.item1.id]))
        self.assertEqual(response.status_code, 200)

        updated_item = self.get_updated_data_for_clone(response)
        updated_name = "CLONE" + updated_item['name'] + " cloned with no WG!"
        updated_item['name'] = updated_name
        updated_item['workgroup'] = ''  # no workgroup this time
        updated_item.update(utils.get_management_forms(self.item1, identifiers=True, slots=True))


        response = self.client.post(reverse('aristotle:clone_item', args=[self.item1.id]), updated_item)

        self.assertTrue(response.status_code == 302)  # make sure its saved ok
        most_recent = response.context[-1]['object']  # Get the item back to check

        self.assertTrue('cloned with no WG' in most_recent.name)
        self.assertTrue(most_recent.workgroup == None)
        self.assertTrue(perms.user_can_view(self.editor, most_recent))

        self.assertRedirects(response, url_slugify_concept(most_recent))
        self.assertEqual(most_recent.name, updated_name)

        # Make sure the right item was saved and our original hasn't been altered.
        self.item1 = self.itemType.objects.get(id=self.item1.id)  # Stupid cache
        self.assertTrue('cloned with no WG' not in self.item1.name)

    def get_updated_data_for_clone(self, response):
        item = response.context['item']

        updating_field = None
        default_fields = {}

        if not hasattr(item, 'serialize_weak_entities'):
            # The model has no weak entities
            return utils.model_to_dict(item)
        else:
            weak_formsets = response.context['weak_formsets']
            weak = item.serialize_weak_entities

            # Serialize the on-field models
            data = utils.model_to_dict_with_change_time(item)

            for pre, value_type in weak:
                # Find associated formset
                current_formset = None
                for formset in weak_formsets:
                    if formset['formset'].prefix == pre:
                        current_formset = formset['formset']

                # Check that a formset with the correct prefix was rendered
                self.assertIsNotNone(current_formset)

                num_vals = getattr(item, value_type).all().count()
                ordering_field = getattr(item, value_type).model.ordering_field

                # Check to make sure the classes with weak entities added them on setUp below
                skipped_fields = ['id', 'ORDER', 'start_date', 'end_date', 'DELETE']

                for i, v in enumerate(getattr(self.item1, value_type).all()):
                    data.update(
                        {"%s-%d-id" % (pre, i): v.pk, "%s-%d-ORDER" % (pre, i): getattr(v, ordering_field)}
                    )

                    data.pop("%s-%d-id" % (pre, i))
                    for field in current_formset[0].fields:
                        if hasattr(v, field) and field not in skipped_fields:
                            value = getattr(v, field)
                            if value is not None:
                                if updating_field is None:
                                    # See if this is the field to update
                                    model_field = current_formset[0]._meta.model._meta.get_field(field)

                                    if isinstance(model_field, CharField) or isinstance(model_field, TextField):
                                        updating_field = field

                                if field == updating_field:
                                    data.update({"%s-%d-%s" % (pre, i, field): value + ' -updated'})
                                else:
                                    added_value = value
                                    if field in default_fields:
                                        data.update({"%s-%d-%s" % (pre, i, field): default_fields[field]})
                                        added_value = default_fields[field]
                                    else:
                                        data.update({"%s-%d-%s" % (pre, i, field): value})
                                    if i == num_vals - 1:
                                        # add a copy
                                        data.update({"%s-%d-%s" % (pre, i + 1, field): added_value})
                    data.pop("%s-%d-id" % (pre, i), None)
                data.update({
                    "%s-TOTAL_FORMS" % pre: num_vals, "%s-INITIAL_FORMS" % 0: num_vals, "%s-MAX_NUM_FORMS" % pre: 1000,
                })
                # Add the management forms for each formset
            return data

    def test_help_page_exists(self):
        self.logout()
        self.load_help()
        response = self.client.get(
            reverse('aristotle_help:concept_help', args=[self.itemType._meta.app_label, self.itemType._meta.model_name])
        )
        self.assertEqual(response.status_code, 200)

    def test_viewer_can_view_registration_history(self):
        self.login_viewer()
        response = self.client.get(reverse('aristotle:registrationHistory', args=[self.item1.id]))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('aristotle:registrationHistory', args=[self.item2.id]))
        self.assertEqual(response.status_code, 403)

    def test_anon_cannot_view_registration_history(self):
        self.logout()
        response = self.client.get(reverse('aristotle:registrationHistory', args=[self.item1.id]))
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('aristotle:registrationHistory', args=[self.item2.id]))
        self.assertEqual(response.status_code, 302)

    def test_viewer_can_view_item_history(self):
        """Test that workgroup members can see the history of items"""
        self.login_viewer()
        response = self.client.get(reverse('aristotle:item_history', args=[self.item1.id]))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('aristotle:item_history', args=[self.item2.id]))
        self.assertEqual(response.status_code, 403)

        # Viewers will even have the link to history on items they are in the workgroup for
        response = self.client.get(self.item1.get_absolute_url())
        self.assertContains(response, reverse('aristotle:item_history', args=[self.item1.id]))

    @tag('changestatus')
    def test_registrar_can_change_status(self):
        self.login_registrar()

        self.make_review_request(self.item1, self.registrar)

        response = self.client.get(reverse('aristotle:changeStatus', args=[self.item1.id]))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(self.item1.statuses.count(), 0)
        response = self.client.post(
            reverse('aristotle:changeStatus', args=[self.item1.id]),
            {
                'change_status-registrationAuthorities': [str(self.ra.id)],
                'change_status-state': self.ra.public_state,
                'change_status-changeDetails': "testing",
                'change_status-cascadeRegistration': 0,  # no
                'submit_skip': 'value',
                'change_status_view-current_step': 'change_status',
            }
        )
        self.assertRedirects(response, url_slugify_concept(self.item1))

        self.item1 = self.itemType.objects.get(pk=self.item1.pk)
        self.assertEqual(self.item1.statuses.count(), 1)
        self.assertTrue(self.item1.is_registered)
        self.assertTrue(self.item1.is_public())

    @tag('inactive_ra', 'changestatus')
    def test_registrar_cant_change_status_with_inactive_ra(self):

        self.login_registrar()
        self.make_review_request(self.item1, self.registrar)

        # Deactivate RA
        self.ra.active = 1
        self.ra.save()

        response = self.client.get(reverse('aristotle:changeStatus', args=[self.item1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.ra in response.context['form'].fields['registrationAuthorities'].queryset)

        response = self.client.post(
            reverse('aristotle:changeStatus', args=[self.item1.id]),
            {
                'change_status-registrationAuthorities': [str(self.ra.id)],
                'change_status-state': self.ra.public_state,
                'change_status-changeDetails': "testing",
                'change_status-cascadeRegistration': 0,  # no
                'submit_skip': 'value',
                'change_status_view-current_step': 'change_status',
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue('registrationAuthorities' in response.context['form'].errors)

    @tag('changestatus')
    @override_settings(ALWAYS_SYNC_REGISTER=True)
    def test_registrar_can_change_status_with_cascade(self):
        if not hasattr(self, "run_cascade_tests"):
            return
        self.login_registrar()

        # Add sub items to another review so we have perm
        self.make_review_request_iterable(
            self.item1.registry_cascade_items,
            self.registrar,
        )

        self.change_status(self.item1, self.registrar, self.ra, cascade=True)

        self.item1 = self.itemType.objects.get(pk=self.item1.pk)
        self.assertEqual(self.item1.statuses.count(), 1)
        self.assertTrue(self.item1.is_registered)
        self.assertTrue(self.item1.is_public())
        for sub_item in self.item1.registry_cascade_items:
            self.assertTrue(sub_item.is_registered)

    @tag('changestatus')
    @override_settings(ALWAYS_SYNC_REGISTER=True)
    def test_registrar_can_change_status_with_cascade_bad_perms(self):
        if not hasattr(self, "run_cascade_tests"):
            return
        self.login_registrar()

        self.change_status(self.item1, self.registrar, self.ra, cascade=True)

        self.item1 = self.itemType.objects.get(pk=self.item1.pk)
        self.assertEqual(self.item1.statuses.count(), 1)
        self.assertTrue(self.item1.is_registered)
        self.assertTrue(self.item1.is_public())
        for sub_item in self.item1.registry_cascade_items:
            self.assertFalse(sub_item.is_registered)

    @tag('changestatus')
    def test_registrar_cannot_use_faulty_statuses(self):
        self.login_registrar()

        self.assertFalse(perms.user_can_view(self.registrar, self.item1))
        self.item1.save()
        self.item1 = self.itemType.objects.get(pk=self.item1.pk)

        self.make_review_request(self.item1, self.registrar)

        self.assertTrue(perms.user_can_view(self.registrar, self.item1))
        self.assertTrue(perms.user_can_add_status(self.registrar, self.item1))

        response = self.client.get(reverse('aristotle:changeStatus', args=[self.item1.id]))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(self.item1.statuses.count(), 0)
        response = self.client.post(
            reverse('aristotle:changeStatus', args=[self.item1.id]),
            {
                'change_status-registrationAuthorities': [str(self.ra.id)],
                'change_status-state': "Not a number",  # obviously wrong
                'change_status-changeDetails': "testing",
                'change_status-cascadeRegistration': 0,  # no
                'submit_skip': 'value',
                'change_status_view-current_step': 'change_status',
            }
        )
        self.assertFormError(response, 'form', 'state',
                             'Select a valid choice. Not a number is not one of the available choices.')

        response = self.client.post(
            reverse('aristotle:changeStatus', args=[self.item1.id]),
            {
                'change_status-registrationAuthorities': [str(self.ra.id)],
                'change_status-state': "343434",  # also wrong
                'change_status-changeDetails': "testing",
                'change_status-cascadeRegistration': 0,  # no
                'submit_skip': 'value',
                'change_status_view-current_step': 'change_status',
            }
        )
        self.assertFormError(response, 'form', 'state',
                             'Select a valid choice. 343434 is not one of the available choices.')

    def registrar_can_change_status_with_review(self, cascade):
        # If not running cascade tests return
        if not hasattr(self, "run_cascade_tests") and cascade:
            return

        self.login_registrar()

        # Make ReviewRequest with item
        review = self.make_review_request(self.item1, self.registrar)

        if cascade:
            # Make ReviewRequest with first sub item so we have permission to change status on it
            self.make_review_request(self.item1.registry_cascade_items[0], self.registrar)

        # Make sure registrar can view and change status of item
        self.assertTrue(perms.user_can_view(self.registrar, self.item1))
        self.assertTrue(perms.user_can_add_status(self.registrar, self.item1))

        # Check item is not registered
        self.assertFalse(self.item1.is_registered)

        if cascade:
            cascade_post = 1
        else:
            cascade_post = 0

        response = self.client.post(
            reverse('aristotle:changeStatus', args=[self.item1.id]),
            {
                'change_status-registrationAuthorities': [str(self.ra.id)],
                'change_status-state': self.ra.public_state,
                'change_status-changeDetails': "testing",
                'change_status-cascadeRegistration': cascade_post,
                'submit_next': 'value',
                'change_status_view-current_step': 'change_status',
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['wizard']['steps'].step1, 2)  # check we are now on second setep

        # On second step, select items we want to change
        selected_for_change = [self.item1.id]
        if cascade:
            selected_for_change.append(self.item1.registry_cascade_items[0].id)

        selected_for_change_strings = [str(a) for a in selected_for_change]

        review_response = self.client.post(
            reverse('aristotle:changeStatus', args=[self.item1.id]),
            {
                'review_changes-selected_list': selected_for_change_strings,
                'change_status_view-current_step': 'review_changes',
            }
        )
        self.assertRedirects(review_response, url_slugify_concept(self.item1))

        self.item1.refresh_from_db()
        self.assertEqual(self.item1.statuses.count(), 1)
        self.assertTrue(self.item1.is_registered)
        self.assertTrue(self.item1.is_public())
        if cascade:
            for sub_item in self.item1.registry_cascade_items:
                # If we selected for change, should be registered otherwise not
                if sub_item.id in selected_for_change:
                    self.assertTrue(sub_item.is_registered)
                else:
                    self.assertFalse(sub_item.is_registered)

    @tag('changestatus')
    @override_settings(ALWAYS_SYNC_REGISTER=True)
    def test_registrar_can_change_status_with_review_cascade(self):
        self.registrar_can_change_status_with_review(cascade=True)

    @tag('changestatus')
    def test_registrar_can_change_status_with_review_no_cascade(self):
        self.registrar_can_change_status_with_review(cascade=False)

    @tag('changestatus')
    def test_viewer_cannot_change_status(self):
        self.login_viewer()

        response = self.client.get(reverse('aristotle:changeStatus', args=[self.item1.id]))
        self.assertEqual(response.status_code, 403)

    @tag('changestatus')
    def test_anon_cannot_change_status(self):
        self.logout()

        response = self.client.get(reverse('aristotle:changeStatus', args=[self.item1.id]))
        self.assertRedirects(response, reverse('friendly_login') + "?next=" + reverse('aristotle:changeStatus',
                                                                                      args=[self.item1.id]))

    @tag('changestatus')
    def test_cascade_action(self):
        self.logout()
        check_url = reverse('aristotle:check_cascaded_states', args=[self.item1.pk])

        response = self.client.get(check_url)
        self.assertEqual(response.status_code, 403)

        self.login_editor()

        response = self.client.get(check_url)
        self.assertEqual(response.status_code, 404)

    def test_weak_editing_in_advanced_editor_dynamic(self, updating_field=None, default_fields={}):
        """Test updating weak entities to the model through edit page formsets

        The test attempts to make an edit to any weak item, but does fail on some types
        Over time we would like to have specific tests on each type instead of this general one
        """

        if hasattr(self.item1, 'serialize_weak_entities'):
            self.login_editor()
            value_url = 'aristotle:edit_item'

            response = self.client.get(reverse(value_url, args=[self.item1.id]))
            self.assertEqual(response.status_code, 200)

            weak_formsets = response.context['weak_formsets']

            weak = self.item1.serialize_weak_entities

            for entity in weak:

                value_type = entity[1]
                pre = entity[0]

                # find associated formset
                current_formset = None
                for formset in weak_formsets:
                    if formset['formset'].prefix == pre:
                        current_formset = formset['formset']

                # check that a formset with the correct prefix was rendered
                self.assertIsNotNone(current_formset)

                data = utils.model_to_dict_with_change_time(self.item1)

                num_vals = getattr(self.item1, value_type).all().count()
                ordering_field = getattr(self.item1, value_type).model.ordering_field

                # check to make sure the classes with weak entities added them on setUp below
                self.assertGreater(num_vals, 0)

                skipped_fields = ['id', 'ORDER', 'start_date', 'end_date', 'DELETE']
                for i, v in enumerate(getattr(self.item1, value_type).all()):
                    data.update({"%s-%d-id" % (pre, i): v.pk, "%s-%d-ORDER" % (pre, i): getattr(v, ordering_field)})
                    for field in current_formset[0].fields:
                        if hasattr(v, field) and field not in skipped_fields:
                            value = getattr(v, field)
                            if value is not None:

                                if (updating_field is None):
                                    # see if this is the field to update
                                    model_field = current_formset[0]._meta.model._meta.get_field(field)

                                    if isinstance(model_field, CharField) or isinstance(model_field, TextField):
                                        updating_field = field

                                if field == updating_field:
                                    data.update({"%s-%d-%s" % (pre, i, field): value + ' -updated'})
                                else:
                                    added_value = value
                                    if field in default_fields:
                                        data.update({"%s-%d-%s" % (pre, i, field): default_fields[field]})
                                        added_value = default_fields[field]
                                    else:
                                        data.update({"%s-%d-%s" % (pre, i, field): value})
                                    if (i == num_vals - 1):
                                        # add a copy
                                        data.update({"%s-%d-%s" % (pre, i + 1, field): added_value})

                self.assertIsNotNone(updating_field)
                # no string was found to update
                # if this happens the test needs to be passed an updating_field or changed to support more
                # than text updates

                i = 0
                data.update({"%s-%d-DELETE" % (pre, i): 'checked', "%s-%d-%s" % (pre, i, updating_field): getattr(v,
                                                                                                                  updating_field) + " - deleted"})  # delete the last one.

                # add order and updating_value to newly added data
                i = num_vals
                data.update({"%s-%d-ORDER" % (pre, i): i, "%s-%d-%s" % (pre, i, updating_field): "new value -updated"})

                # add management form
                data.update({
                    "%s-TOTAL_FORMS" % pre: num_vals + 1, "%s-INITIAL_FORMS" % pre: num_vals,
                    "%s-MAX_NUM_FORMS" % pre: 1000,
                })

                response = self.client.post(reverse(value_url, args=[self.item1.id]), data)
                self.assertEqual(response.status_code, self.Status.FOUND)

                self.item1 = self.itemType.objects.get(pk=self.item1.pk)

                self.assertTrue(num_vals == getattr(self.item1, value_type).all().count())

                new_value_seen = False
                for v in getattr(self.item1, value_type).all():
                    value = getattr(v, updating_field)
                    self.assertTrue('updated' in value)  # This will fail if the item isn't updated
                    self.assertFalse('deleted' in value)  # make sure deleted value not present
                    if value == 'new value -updated':
                        new_value_seen = True
                self.assertTrue(new_value_seen)

    @tag('version')
    def test_view_previous_version_from_item_version(self):

        old_definition = self.item1.definition

        self.update_definition_with_versions()

        versions = reversion.models.Version.objects.get_for_object(self.item1)
        self.assertEqual(versions.count(), 2)
        oldest_version = versions.last()

        self.login_viewer()
        response = self.reverse_get(
            'aristotle:item_version',
            reverse_args=[oldest_version.id],
            status_code=200
        )

        fields = {f.heading: f for f in response.context['item']['item_fields']}
        self.assertTrue('Definition' in fields)
        dfn_field = fields['Definition']
        self.assertEqual(dfn_field.value, old_definition)

    @tag('download')
    @override_settings(
        ARISTOTLE_SETTINGS={"DOWNLOAD_OPTIONS": {'DOWNLOADERS': ['aristotle_mdr.downloaders.HTMLDownloader']}})
    def test_download_content(self):
        downloader = HTMLDownloader([self.item1.id], self.editor.id, {})
        html = downloader.get_html().decode()
        self.assertTrue(len(html) > 0)
        self.assertTrue(self.item1.definition in html)


class ObjectClassViewPage(LoggedInViewConceptPages, TestCase):
    itemType = MDR.ObjectClass


class PropertyViewPage(LoggedInViewConceptPages, TestCase):
    itemType = MDR.Property


class UnitOfMeasureViewPage(LoggedInViewConceptPages, TestCase):
    itemType = MDR.UnitOfMeasure


class ValueDomainViewPage(LoggedInViewConceptPages, TestCase):
    itemType = MDR.ValueDomain

    def setUp(self):
        super().setUp()

        for i in range(4):
            MDR.PermissibleValue.objects.create(
                value=i, meaning="test permissible meaning %d" % i, order=i, valueDomain=self.item1
            )
        for i in range(4):
            MDR.SupplementaryValue.objects.create(
                value=i, meaning="test supplementary meaning %d" % i, order=i, valueDomain=self.item1
            )

        # Data used to test value domain conceptual domain link
        cd = MDR.ConceptualDomain.objects.create(
            description='test description'
        )

        cd2 = MDR.ConceptualDomain.objects.create(
            description='unrelated conceptual domain'
        )
        MDR.ValueMeaning.objects.create(
            name="test name",
            definition="test definition",
            conceptual_domain=cd2,
            order=0,
        )

        self.vms = []
        for i in range(2):
            vm = MDR.ValueMeaning.objects.create(
                name="test name",
                definition="test definition",
                conceptual_domain=cd,
                order=i,
            )
            self.vms.append(vm)

        self.item3.conceptual_domain = cd
        self.item3.save()

    def test_weak_editing_in_advanced_editor_dynamic(self):
        super().test_weak_editing_in_advanced_editor_dynamic(updating_field='value')

    def submitter_user_can_use_value_edit_page(self, value_type):
        value_url = 'aristotle:edit_item'

        self.login_editor()

        data = utils.model_to_dict_with_change_time(self.item1)
        num_vals = getattr(self.item1, value_type + "Values").count()
        i = 0
        for i, v in enumerate(getattr(self.item1, value_type + "Values").all()):
            data.update({
                "%s_values-%d-valueDomain" % (value_type, i): self.item1.pk,
                "%s_values-%d-id" % (value_type, i): v.pk,
                "%s_values-%d-ORDER" % (value_type, i): v.order,
                "%s_values-%d-value" % (value_type, i): v.value,
                "%s_values-%d-meaning" % (value_type, i): v.meaning + " -updated"
            })
        data.update({
            "%s_values-%d-DELETE" % (value_type, i): 'checked',
            "%s_values-%d-meaning" % (value_type, i): v.meaning + " - deleted",
            "%s_values-%d-valueDomain" % (value_type, i): self.item1.pk,
        })  # delete the last one.
        # now add a new one
        i = i + 1
        data.update({
            "%s_values-%d-ORDER" % (value_type, i): i,
            "%s_values-%d-value" % (value_type, i): 100,
            "%s_values-%d-meaning" % (value_type, i): "new value (also an updated value)",
            "%s_values-%d-valueDomain" % (value_type, i): self.item1.pk,
        })

        data.update({
            "%s_values-TOTAL_FORMS" % (value_type): i + 1,
            "%s_values-INITIAL_FORMS" % (value_type): num_vals,
            "%s_values-MAX_NUM_FORMS" % (value_type): 1000,
        })

        response = self.client.post(reverse(value_url, args=[self.item1.id]), data)
        self.assertEqual(response.status_code, 302)
        self.item1 = MDR.ValueDomain.objects.get(pk=self.item1.pk)

        self.assertEqual(num_vals, getattr(self.item1, value_type + "Values").count())
        new_value_seen = False
        for v in getattr(self.item1, value_type + "Values").all():
            self.assertTrue('updated' in v.meaning)  # This will fail if the deleted item isn't deleted
            if v.value == '100' and "new value" in v.meaning:
                new_value_seen = True
        self.assertTrue(new_value_seen)

        # Item is now locked, submitter is no longer able to edit
        MDR.Status.objects.create(
            concept=self.item1,
            registrationAuthority=self.ra,
            registrationDate=timezone.now(),
            state=self.ra.locked_state
        )

        self.item1 = MDR.ValueDomain.objects.get(pk=self.item1.pk)
        self.assertTrue(self.item1.is_locked())
        self.assertFalse(perms.user_can_edit(self.editor, self.item1))

    def test_submitter_can_use_permissible_value_edit_page(self):
        self.submitter_user_can_use_value_edit_page('permissible')

    def test_submitter_can_use_supplementary_value_edit_page(self):
        self.submitter_user_can_use_value_edit_page('supplementary')

    def test_submitter_user_doesnt_save_all_blank_permissible_value_edit_page(self):
        self.submitter_user_doesnt_save_all_blank('permissible')

    def test_submitter_user_doesnt_save_all_blank_supplementary_value_edit_page(self):
        self.submitter_user_doesnt_save_all_blank('supplementary')

    def submitter_user_doesnt_save_all_blank(self, value_type):
        value_url = 'aristotle:edit_item'

        self.login_editor()

        data = utils.model_to_dict_with_change_time(self.item1)
        num_vals = getattr(self.item1, value_type + "Values").count()

        i = 0
        for i, v in enumerate(getattr(self.item1, value_type + "Values").all()):
            data.update({
                "%s_values-%d-valueDomain" % (value_type, i): self.item1.pk,
                "%s_values-%d-id" % (value_type, i): v.pk,
                "%s_values-%d-ORDER" % (value_type, i): v.order,
                "%s_values-%d-value" % (value_type, i): v.value,
                "%s_values-%d-meaning" % (value_type, i): v.meaning + " -updated"
            })

        # now add two new values that are all blank
        i = i + 1
        data.update({"%s_values-%d-ORDER" % (value_type, i): i, "%s_values-%d-value" % (value_type, i): '',
                     "%s_values-%d-meaning" % (value_type, i): ""})
        i = i + 1
        data.update({"%s_values-%d-ORDER" % (value_type, i): i, "%s_values-%d-value" % (value_type, i): '',
                     "%s_values-%d-meaning" % (value_type, i): ""})

        data.update({
            "%s_values-TOTAL_FORMS" % (value_type): i + 1,
            "%s_values-INITIAL_FORMS" % (value_type): num_vals,
            "%s_values-MAX_NUM_FORMS" % (value_type): 1000,
        })
        self.client.post(reverse(value_url, args=[self.item1.id]), data)
        self.item1 = MDR.ValueDomain.objects.get(pk=self.item1.pk)

        self.assertTrue(num_vals == getattr(self.item1, value_type + "Values").count())

    def test_values_shown_on_page(self):
        self.login_viewer()

        response = self.client.get(self.get_page(self.item1))
        self.assertEqual(response.status_code, 200)
        for pv in self.item1.permissiblevalue_set.all():
            self.assertContains(response, pv.meaning, 1)
        for sv in self.item1.supplementaryvalue_set.all():
            self.assertContains(response, sv.meaning, 1)

    @skip('Not fixed yet')
    def test_conceptual_domain_selection(self):
        self.login_editor()
        url = 'aristotle:edit_item'

        response = self.client.get(reverse(url, args=[self.item3.id]))
        self.assertEqual(response.status_code, 200)

        # check queryset correctly filled from conceptual domain for item 2
        formset = response.context['weak_formsets'][0]['formset']
        form = formset.empty_form

        self.assertFalse('meaning' in form.fields.keys())
        self.assertTrue('value_meaning' in form.fields.keys())
        queryset = form.fields['value_meaning'].queryset
        self.assertEqual(queryset.count(), 2)
        for item in queryset:
            self.assertTrue(item in self.vms)

        # Check empty queryset for item 1 (no cd linked)
        response = self.client.get(reverse(url, args=[self.item1.id]))
        self.assertEqual(response.status_code, 200)

        formset = response.context['weak_formsets'][0]['formset']
        for form in formset:
            self.assertFalse('value_meaning' in form.fields.keys())
            self.assertTrue('meaning' in form.fields.keys())

    @tag('version')
    def test_version_display_of_values(self):
        self.update_definition_with_versions()

        latest = reversion.models.Version.objects.get_for_object(self.item1).last()

        self.login_viewer()
        response = self.reverse_get(
            'aristotle:item_version',
            reverse_args=[latest.id],
            status_code=200
        )

        fields = {f.heading: f for f in response.context['item']['item_fields']}
        self.assertTrue('Supplementary Values' in fields)
        self.assertTrue('Permissible Values' in fields)

        subval_field = fields['Supplementary Values']
        permval_field = fields['Permissible Values']

        self.assertTrue(subval_field.is_group)
        self.assertTrue(permval_field.is_group)

        first_pval = {f.heading: f for f in permval_field.sub_fields[0]}
        first_sval = {f.heading: f for f in subval_field.sub_fields[0]}

        # Check supplementary values are being displayed
        self.assertEqual(first_sval['Meaning'].value, 'test supplementary meaning 0')
        self.assertEqual(first_sval['Meaning'].is_link, False)

        self.assertEqual(first_pval['Meaning'].value, 'test permissible meaning 0')
        self.assertEqual(first_pval['Meaning'].is_link, False)

    @skip('Currently no serializing value meanings')
    @tag('version')
    def test_version_display_of_value_meanings(self):

        vm = self.vms[0]

        MDR.PermissibleValue.objects.create(
            value='1',
            value_meaning=vm,
            order=0,
            valueDomain=self.item3
        )

        with reversion.create_revision():
            self.item3.save()

        latest = reversion.models.Version.objects.get_for_object(self.item3).last()

        self.login_viewer()
        response = self.reverse_get(
            'aristotle:item_version',
            reverse_args=[latest.id],
            status_code=200
        )

        weak_context = response.context['item']['weak']
        perm_values = weak_context[0]['items']

        self.assertEqual(weak_context[0]['model'], 'Permissible Value')

        self.assertTrue(perm_values[0]['Value Meaning'].is_link)
        self.assertEqual(perm_values[0]['Value Meaning'].obj, vm)
        self.assertEqual(perm_values[0]['Value Meaning'].link_id, self.item3.conceptual_domain.id)

    @tag('clone_item')
    def test_clone_vd_with_components(self):
        self.login_editor()
        old_name = self.item1.name
        response = self.client.get(reverse('aristotle:clone_item', args=[self.item1.id]))
        self.assertEqual(response.status_code, 200)
        data = self.get_updated_data_for_clone(response)
        data.update({
            'name': 'Goodness (clone)',
            'definition': 'A measure of good'
        })

        response = self.client.post(reverse('aristotle:clone_item', args=[self.item1.id]), data)

        clone = response.context[-1]['object']  # Get the item back to check
        self.item1 = MDR.ValueDomain.objects.get(pk=self.item1.pk)
        clone = MDR.ValueDomain.objects.get(pk=clone.pk)
        self.assertTrue(clone.pk != self.item1.id)

        # clone = models.ValueDomain.objects.get(name='Goodness (clone)')

        self.assertEqual(clone.name, 'Goodness (clone)')
        self.assertEqual(self.item1.name, old_name)
        self.assertEqual(clone.permissiblevalue_set.count(), 4)
        self.assertEqual(clone.supplementaryvalue_set.count(), 4)

    def create_bulk_values(self, n: int, vd):
        pvs = []
        for i in range(n):
            value = 'Value {}'.format(i),
            meaning = 'Meaning {}'.format(i),
            pv = MDR.PermissibleValue(
                valueDomain=vd,
                value=value,
                meaning=meaning,
                order=i
            )
            pvs.append(pv)
        MDR.PermissibleValue.objects.bulk_create(pvs)

    def post_and_time_permissible_values(self, vd, data, datalist, initial, event_name):
        permdata = self.get_formset_postdata(datalist, 'permissible_values', initial)
        data.update(permdata)

        self.login_editor()

        self.start_timer()
        response = self.client.post(
            reverse('aristotle:edit_item', args=[vd.id]),
            data
        )
        self.end_timer(event_name)
        self.assertEqual(response.status_code, 302)

    @tag('bulk_values', 'slow')
    def test_create_bulk_values(self):
        vd = MDR.ValueDomain.objects.create(
            name='Lots of values',
            definition='Lots',
            submitter=self.editor
        )
        data = utils.model_to_dict_with_change_time(vd)

        datalist = []
        for i in range(100):
            datalist.append({
                'value': 'Value {}'.format(i),
                'meaning': 'Meaning {}'.format(i),
                'valueDomain': vd.id,
                'ORDER': i
            })

        self.post_and_time_permissible_values(vd, data, datalist, 0, 'CREATE')
        vd = MDR.ValueDomain.objects.get(id=vd.id)
        self.assertEqual(vd.permissiblevalue_set.count(), 100)

    @tag('bulk_values', 'slow')
    def test_reorder_bulk_values(self):
        vd = MDR.ValueDomain.objects.create(
            name='Lots of values',
            definition='Lots',
            submitter=self.editor
        )
        data = utils.model_to_dict_with_change_time(vd)

        self.create_bulk_values(1000, vd)

        datalist = []
        for pv in vd.permissiblevalue_set.all():
            datalist.append({
                'id': pv.id,
                'value': pv.value,
                'meaning': pv.meaning,
                'valueDomain': vd.id,
                'ORDER': pv.order + 1
            })

        self.post_and_time_permissible_values(vd, data, datalist, 1000, 'REORDER')
        vd = MDR.ValueDomain.objects.get(id=vd.id)
        self.assertEqual(vd.permissiblevalue_set.count(), 1000)

    @tag('bulk_values', 'slow')
    def test_delete_bulk_values(self):
        vd = MDR.ValueDomain.objects.create(
            name='Lots of values',
            definition='Lots',
            submitter=self.editor
        )
        data = utils.model_to_dict_with_change_time(vd)

        self.create_bulk_values(100, vd)

        datalist = []
        for pv in vd.permissiblevalue_set.all():
            datalist.append({
                'id': pv.id,
                'value': pv.value,
                'meaning': pv.meaning,
                'valueDomain': vd.id,
                'ORDER': pv.order,
                'DELETE': 'checked'
            })

        self.post_and_time_permissible_values(vd, data, datalist, 100, 'DELETE')
        vd = MDR.ValueDomain.objects.get(id=vd.id)
        self.assertEqual(vd.permissiblevalue_set.count(), 0)


class ConceptualDomainViewPage(LoggedInViewConceptPages, TestCase):
    itemType = MDR.ConceptualDomain

    def setUp(self):
        super().setUp()

        for i in range(4):
            MDR.ValueMeaning.objects.create(
                name="test name",
                definition="test definition",
                conceptual_domain=self.item1,
                order=i,
            )

    @tag('edit_formsets')
    def test_edit_formset_error_display(self):
        self.login_editor()

        edit_url = 'aristotle:edit_item'
        response = self.client.get(reverse(edit_url, args=[self.item1.id]))
        self.assertEqual(response.status_code, 200)

        data = utils.model_to_dict_with_change_time(self.item1)

        # submit an item with a blank name
        valuemeaning_formset_data = [
            {'name': '', 'definition': 'test defn', 'start_date': '1999-01-01', 'end_date': '2090-01-01', 'ORDER': 0},
            {'name': 'Test2', 'definition': 'test defn', 'start_date': '1999-01-01', 'end_date': '2090-01-01',
             'ORDER': 1}
        ]
        data.update(self.get_formset_postdata(valuemeaning_formset_data, 'value_meaning', 0))
        response = self.client.post(reverse(edit_url, args=[self.item1.id]), data)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context['weak_formsets'][0]['formset'].errors[0],
                         {'name': ['This field is required.']})
        self.assertContains(response, 'This field is required.')


class DataElementConceptViewPage(LoggedInViewConceptPages, TestCase):
    itemType = MDR.DataElementConcept
    run_cascade_tests = True

    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.oc = MDR.ObjectClass.objects.create(
            name="sub item OC",
            workgroup=self.item1.workgroup,
        )
        self.prop = MDR.Property.objects.create(
            name="sub item prop",
            workgroup=self.item1.workgroup
        )
        self.item1.objectClass = self.oc
        self.item1.property = self.prop
        self.item1.save()
        self.assertTrue(self.oc.can_view(self.editor))
        self.assertTrue(self.prop.can_view(self.editor))

    def test_foreign_key_popups(self):
        self.logout()

        check_url = reverse('aristotle:generic_foreign_key_editor', args=[self.item1.pk, 'objectclassarino'])
        response = self.client.get(check_url)
        self.assertEqual(response.status_code, 404)

        check_url = reverse('aristotle:generic_foreign_key_editor', args=[self.item1.pk, 'objectclass'])
        response = self.client.get(check_url)
        self.assertEqual(response.status_code, 302)  # user must login too see

        response = self.client.post(check_url, {'objectClass': ''})
        self.assertEqual(response.status_code, 302)
        self.item1 = self.item1.__class__.objects.get(pk=self.item1.pk)
        self.assertTrue(self.item1.objectClass is not None)

        self.login_editor()
        response = self.client.get(check_url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(check_url, {'objectClass': ''})
        self.assertEqual(response.status_code, 302)
        self.item1 = self.item1.__class__.objects.get(pk=self.item1.pk)
        self.assertTrue(self.item1.objectClass is None)

        response = self.client.post(check_url, {'objectClass': self.prop.pk})
        self.assertEqual(response.status_code, 200)
        self.item1 = self.item1.__class__.objects.get(pk=self.item1.pk)
        self.assertTrue(self.item1.objectClass is None)

        another_oc = MDR.ObjectClass.objects.create(
            name="editor can't see this",
            definition="my definition",
        )
        response = self.client.post(check_url, {'objectClass': another_oc.pk})
        self.assertEqual(response.status_code, 200)
        self.item1 = self.item1.__class__.objects.get(pk=self.item1.pk)
        self.assertTrue(self.item1.objectClass is None)

        response = self.client.post(check_url, {'objectClass': self.oc.pk})
        self.assertEqual(response.status_code, 302)
        self.item1 = self.item1.__class__.objects.get(pk=self.item1.pk)
        self.assertTrue(self.item1.objectClass == self.oc)

    def test_regular_cannot_save_a_property_they_cant_see_via_edit_page(self):
        self.login_regular_user()
        self.regular_item = self.itemType.objects.create(name="regular item", definition="my definition",
                                                         submitter=self.regular, **self.defaults)
        response = self.client.get(reverse('aristotle:edit_item', args=[self.regular_item.id]))
        self.assertEqual(response.status_code, 200)

        updated_item = utils.model_to_dict_with_change_time(response.context['item'])
        updated_name = updated_item['name'] + " updated!"
        updated_item['name'] = updated_name

        different_prop = MDR.Property.objects.create(
            name="sub item prop 2",
            workgroup=self.item1.workgroup
        )
        updated_item['property'] = different_prop.pk

        self.assertFalse(self.prop.can_view(self.regular))
        self.assertFalse(different_prop.can_view(self.regular))

        response = self.client.post(reverse('aristotle:edit_item', args=[self.regular_item.id]), updated_item)
        self.regular_item = self.itemType.objects.get(pk=self.regular_item.pk)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('not one of the available choices' in response.context['form'].errors['property'][0])
        self.assertFalse(self.regular_item.name == updated_name)
        self.assertFalse(self.regular_item.property == self.prop)

    def test_cascade_action(self):
        self.logout()
        check_url = reverse('aristotle:check_cascaded_states', args=[self.item1.pk])

        response = self.client.get(check_url)
        self.assertEqual(response.status_code, 403)

        self.login_editor()

        response = self.client.get(check_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.item1.objectClass.name)
        self.assertContains(response, self.item1.property.name)

        ra = MDR.RegistrationAuthority.objects.create(name="new RA", stewardship_organisation=self.steward_org)
        item = self.item1.property
        s = MDR.Status.objects.create(
            concept=item,
            registrationAuthority=ra,
            registrationDate=timezone.now(),
            state=ra.locked_state
        )
        s = MDR.Status.objects.create(
            concept=item,
            registrationAuthority=self.ra,
            registrationDate=timezone.now(),
            state=ra.locked_state
        )
        s = MDR.Status.objects.create(
            concept=self.item1,
            registrationAuthority=self.ra,
            registrationDate=timezone.now(),
            state=ra.public_state
        )

        response = self.client.get(check_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.item1.objectClass.name)
        self.assertContains(response, self.item1.property.name)
        self.assertContains(response, 'fa-times')  # The property has a different status

    def test_user_can_not_see_sub_components_without_permission(self):
        self.prop.workgroup = self.wg2
        self.prop.save()
        self.assertTrue(perms.user_can_view(self.viewer, self.item1))
        self.assertFalse(perms.user_can_view(self.viewer, self.prop))

        self.login_viewer()
        response = self.reverse_get(
            'aristotle:item',
            reverse_args=[self.item1.id, 'dataelementconcept', 'name'],
            status_code=200
        )
        self.assertNotContains(response, self.prop.name)


class DataElementViewPage(LoggedInViewConceptPages, TestCase):
    itemType = MDR.DataElement

    def add_dec(self, wg):
        dec = MDR.DataElementConcept.objects.create(
            name='test dec',
            definition='just a test',
            workgroup=wg
        )
        self.item1.dataElementConcept = dec
        self.item1.save()

    def test_cascade_action(self):
        self.logout()
        check_url = reverse('aristotle:check_cascaded_states', args=[self.item1.pk])
        self.dec1 = MDR.DataElementConcept.objects.create(name='DEC1 - visible', definition="my definition",
                                                          workgroup=self.wg1)
        self.item1.dataElementConcept = self.dec1
        self.item1.save()

        response = self.client.get(check_url)
        self.assertEqual(response.status_code, 403)

        self.login_editor()

        response = self.client.get(check_url)
        self.assertEqual(response.status_code, 200)

    @tag('version')
    def test_version_display_components(self):
        self.add_dec(self.wg1)
        self.update_definition_with_versions()

        latest = reversion.models.Version.objects.get_for_object(self.item1).first()

        self.login_viewer()
        response = self.reverse_get(
            'aristotle:item_version',
            reverse_args=[latest.id],
            status_code=200
        )

        fields = {f.heading: f for f in response.context['item']['item_fields']}
        self.assertTrue('Data Element Concept' in fields)
        cfield = fields['Data Element Concept']

        self.assertTrue(cfield.is_link)
        self.assertEqual(cfield.obj_name, self.item1.dataElementConcept.name)
        self.assertEqual(cfield.id, self.item1.dataElementConcept.id)

    @tag('version')
    def test_version_display_component_from_multi_revision(self):
        dec1 = MDR.DataElementConcept.objects.create(
            name='dec1',
            definition='just a test',
            workgroup=self.wg1
        )

        dec2 = MDR.DataElementConcept.objects.create(
            name='dec2',
            definition='just a test',
            workgroup=self.wg1
        )

        self.item1.dataElementConcept = dec1
        self.item2.dataElementConcept = dec2

        with reversion.create_revision():
            self.item1.save()
            self.item2.save()

        latest = reversion.models.Version.objects.get_for_object(self.item1).first()

        self.login_editor()
        response = self.reverse_get(
            'aristotle:item_version',
            reverse_args=[latest.id],
            status_code=200
        )

        fields = {f.heading: f for f in response.context['item']['item_fields']}
        self.assertTrue('Data Element Concept' in fields)
        cfield = fields['Data Element Concept']

        self.assertTrue(cfield.is_link)
        self.assertEqual(cfield.obj_name, self.item1.dataElementConcept.name)
        self.assertEqual(cfield.id, self.item1.dataElementConcept.id)

    @tag('version')
    def test_version_display_component_permission(self):
        """Test that linked objects that are not visible to the user are not displayed"""
        self.add_dec(wg=None)
        self.update_definition_with_versions()

        latest = reversion.models.Version.objects.get_for_object(self.item1).first()
        self.login_viewer()
        response = self.reverse_get(
            'aristotle:item_version',
            reverse_args=[latest.id],
            status_code=200
        )

        fields = {f.heading: f for f in response.context['item']['item_fields']}
        self.assertTrue('Data Element Concept' in fields)
        cfield = fields['Data Element Concept']

        self.assertTrue(cfield.is_link)
        self.assertEqual(cfield.id, self.item1.dataElementConcept.id)
        self.assertEqual(str(cfield), VersionLinkField.perm_message)


class DataElementDerivationViewPage(LoggedInViewConceptPages, TestCase):
    itemType = MDR.DataElementDerivation

    def get_through_model(self, formset_prefix: str) -> Type[MDR.DedBaseThrough]:
        """Get through model based on formset prefix"""
        if formset_prefix == 'inputs':
            return MDR.DedInputsThrough

        return MDR.DedDerivesThrough

    def create_linked_ded(self):
        self.de1 = MDR.DataElement.objects.create(
            name='DE1 Name',
            definition="my definition",
            workgroup=self.wg1
        )
        self.de2 = MDR.DataElement.objects.create(
            name='DE2 Name',
            definition="my definition",
            workgroup=self.wg1
        )
        self.de3 = MDR.DataElement.objects.create(
            name='DE3 Name',
            definition="my definition",
            workgroup=self.wg1
        )

        self.ded = MDR.DataElementDerivation.objects.create(
            name='DED Name',
            definition='my definition',
            workgroup=self.wg1
        )

        ded_derives_1 = MDR.DedDerivesThrough.objects.create(data_element_derivation=self.ded, data_element=self.de1,
                                                             order=0
        )
        ded_derives_2 = MDR.DedDerivesThrough.objects.create(data_element_derivation=self.ded, data_element=self.de2,
                                                             order=1
        )
        ded_derives_3 = MDR.DedDerivesThrough.objects.create(data_element_derivation=self.ded, data_element=self.de3,
                                                             order=2)

        ded_inputs_1 = MDR.DedInputsThrough.objects.create(data_element_derivation=self.ded, data_element=self.de3,
                                                           order=0
        )
        ded_inputs_2 = MDR.DedInputsThrough.objects.create(data_element_derivation=self.ded, data_element=self.de2,
                                                           order=1
        )
        ded_inputs_3 = MDR.DedInputsThrough.objects.create(data_element_derivation=self.ded, data_element=self.de1,
                                                           order=2)

        return self.ded

    def test_weak_editing_in_advanced_editor_dynamic(self):
        """Test editing of ded inputs and derives

        Overrides general weak editor test
        """
        self.login_editor()
        ded = self.create_linked_ded()

        de = MDR.DataElement.objects.create(
            name='Brand new data element',
            definition='So new',
            workgroup=self.wg1,
        )

        inputs = ded.dedinputsthrough_set.all()
        derives = ded.dedderivesthrough_set.all()

        # Serialize item
        data = model_to_dict_with_change_time(ded)

        inputs_data = self.bulk_serialize_inclusions(inputs, ['data_element_derivation'])
        for item in inputs_data:
            item['data_element'] = de.id
        data.update(self.get_formset_postdata(inputs_data, 'inputs', 3))

        derives_data = self.bulk_serialize_inclusions(derives, ['data_element_derivation'])
        for item in derives_data:
            item['data_element'] = de.id
        data.update(self.get_formset_postdata(inputs_data, 'derives', 3))

        # Post edit
        response = self.client.post(
            reverse('aristotle:edit_item', args=[ded.id]),
            data
        )
        self.assertEqual(response.status_code, 302)

        # Check updates were applied
        self.assertEqual(ded.dedinputsthrough_set.count(), 3)
        for item in ded.dedinputsthrough_set.all():
            self.assertEqual(item.data_element, de)

        self.assertEqual(ded.dedderivesthrough_set.count(), 3)
        for item in ded.dedderivesthrough_set.all():
            self.assertEqual(item.data_element, de)

    def check_invalid_type_inputs(self, formset_prefix):
        """Test that a non data element model cannot be added with formset

        Util function used for below tests
        """
        self.login_editor()
        de = MDR.DataElement.objects.create(
            name='Data Element',
            definition='Data Element',
            workgroup=self.wg1,
        )
        oc = MDR.ObjectClass.objects.create(
            name='Object',
            definition='Object',
            workgroup=self.wg1
        )
        self.oc1 = MDR.ObjectClass.objects.create(name='OC - visible but wrong', definition="my definition",
                                                  workgroup=self.wg1)

        data = model_to_dict_with_change_time(self.item1)

        formset_data = [
            {'data_element': de.id, 'ORDER': 0},
            {'data_element': oc.id, 'ORDER': 1},
        ]
        data.update(self.get_formset_postdata(formset_data, formset_prefix))

        response = self.client.post(
            reverse('aristotle:edit_item', args=[self.item1.id]),
            data
        )
        self.assertEqual(response.status_code, self.Status.OK)
        self.assertContains(response, 'Select a valid choice')

        through_model = self.get_through_model(formset_prefix)
        self.assertEqual(
            through_model.objects.filter(data_element_derivation=self.item1).count(), 0
        )

    def test_invalid_type_inputs(self):
        """Test that a non data element model cannot be added as an input"""
        self.check_invalid_type_inputs('inputs')

    def test_invalid_type_derives(self):
        """Test that a non data element model cannot be added as a derive"""
        self.check_invalid_type_inputs('derives')

    def check_submit_non_viewable_de(self, formset_prefix):
        """Check that a data element submitted must be viewable by user

        Util function used by tests below
        """
        self.login_editor()
        # Create de with wrong workgroup
        de = MDR.DataElement.objects.create(
            name='Data',
            definition='Element',
            workgroup=self.wg2
        )
        self.assertFalse(perms.user_can_view(self.editor, de))

        formset_data = [
            {'data_element': de.id, 'ORDER': 0},
            {'data_element': de.id, 'ORDER': 1},
        ]
        data = model_to_dict_with_change_time(self.item1)
        data.update(self.get_formset_postdata(formset_data, formset_prefix))

        response = self.client.post(
            reverse('aristotle:edit_item', args=[self.item1.id]),
            data
        )
        self.assertEqual(response.status_code, self.Status.OK)

        self.assertContains(response, 'Select a valid choice')
        through_model = self.get_through_model(formset_prefix)
        self.assertEqual(
            through_model.objects.filter(data_element_derivation=self.item1).count(), 0
        )

    def test_submit_non_viewable_de_input(self):
        """Check that a data element submitted must be viewable by user to be input"""
        self.check_submit_non_viewable_de('inputs')

    def test_submit_non_viewable_de_derive(self):
        """Check that a data element submitted must be viewable by user to be derived"""
        self.check_submit_non_viewable_de('derives')

    def check_reorder_inputs_with_delete(self, formset_prefix):
        """Check reordering formset while deleting some items

        Util function used for other tests
        """
        self.login_editor()

        # Create data elements for linking
        de = MDR.DataElement.objects.create(
            name='Data1',
            definition='Element1',
            workgroup=self.wg1
        )

        # Get through model
        through_model = self.get_through_model(formset_prefix)

        # Create through model
        instances = []
        for i in range(3):
            through = through_model.objects.create(
                order=i,
                data_element_derivation=self.item1,
                data_element=de,
            )
            instances.append(through)

        # Serialize data
        formset_data = self.bulk_serialize_inclusions(instances, ['data_element_derivation'])
        # Make changes
        formset_data[0]['DELETE'] = 'checked'
        formset_data[1]['ORDER'] = 2
        formset_data[2]['ORDER'] = 1

        # Create submission data
        data = model_to_dict_with_change_time(self.item1)
        data.update(self.get_formset_postdata(formset_data, formset_prefix, 3))

        # Submit
        response = self.client.post(
            reverse('aristotle:edit_item', args=[self.item1.id]),
            data
        )
        self.assertEqual(response.status_code, self.Status.FOUND)

        items = through_model.objects.filter(data_element_derivation=self.item1)
        # Check we only have 2 items now
        self.assertEqual(items.count(), 2)

        # Check order was updated
        second_item = through_model.objects.get(id=formset_data[1]['id'])
        self.assertEqual(second_item.order, 2)

        third_item = through_model.objects.get(id=formset_data[2]['id'])
        self.assertEqual(third_item.order, 1)

    def test_reorder_inputs_with_delete(self):
        self.check_reorder_inputs_with_delete('inputs')

    def test_reorder_derives_with_delete(self):
        self.check_reorder_inputs_with_delete('derives')

    def test_derivation_item_page(self):
        ded = self.create_linked_ded()

        self.login_editor()
        response = self.client.get(reverse("aristotle:item", args=[ded.pk]), follow=True)

        self.assertEqual(response.status_code, 200)

        # Check the template tag that was used returned the correct data

        item = response.context['item']

    @skip('to be fixed in future')
    @tag('ded_version')
    def test_derivation_version_follow(self):

        ded = self.create_linked_ded()

        with reversion.create_revision():
            ded.save()

        versions = reversion.models.Version.objects.get_for_object(ded)
        self.assertEqual(versions.count(), 1)

        version = versions.first()

        data = json.loads(version.serialized_data)
        self.assertEqual(len(data), 1)

        self.assertTrue('derivation_rule' in data[0]['fields'])
        self.assertTrue('derives' in data[0]['fields'])
        self.assertTrue('inputs' in data[0]['fields'])


class LoggedInViewManagedItemPages(utils.LoggedInViewPages):
    defaults = {}

    def setUp(self):
        super().setUp()
        self.item1 = self.itemType.objects.create(
            name="Object 1",
            stewardship_organisation=self.steward_org_1,
            **self.defaults
        )

    def get_page(self, item):
        return item.get_absolute_url()

    def test_help_page_exists(self):
        self.logout()
        # response = self.client.get(self.get_help_page())
        # self.assertEqual(response.status_code,200)

    def test_item_page_exists(self):
        self.logout()
        self.login_superuser()
        response = self.client.get(self.get_page(self.item1))
        self.assertEqual(response.status_code, 200)

    def test_item_page_viewable_when_published(self):
        self.logout()
        response = self.client.get(self.get_page(self.item1))
        self.assertEqual(response.status_code, 403)

        from aristotle_mdr.contrib.publishing import models
        from aristotle_mdr.constants import visibility_permission_choices

        publication_details = models.PublicationRecord.objects.create(
            content_type=ContentType.objects.get_for_model(self.item1),
            object_id=self.item1.pk,
            permission=visibility_permission_choices.auth,
            publication_date=(datetime.datetime.today() - datetime.timedelta(days=2)).date(),
            publisher=self.su
        )

        # User is not logged in, can not see page
        response = self.client.get(self.get_page(self.item1))
        self.assertEqual(response.status_code, 403)

        self.login_viewer()

        # Now logged in, can see page
        response = self.client.get(self.get_page(self.item1))
        self.assertEqual(response.status_code, 200)

        self.logout()

        publication_details.permission = visibility_permission_choices.public
        publication_details.save()

        # Publication now public, can see when logged out
        response = self.client.get(self.get_page(self.item1))
        self.assertEqual(response.status_code, 200)


class MeasureViewPage(LoggedInViewManagedItemPages, TestCase):
    itemType = MDR.Measure


class RegistrationAuthorityViewPage(utils.LoggedInViewPages, TestCase):
    itemType = MDR.RegistrationAuthority

    def setUp(self):
        super().setUp()

        self.item1 = self.itemType.objects.create(
            name="Object 1",
            stewardship_organisation=self.steward_org_1,
        )

        self.item2 = MDR.DataElement.objects.create(name="OC1", workgroup=self.wg1)

        MDR.Status.objects.create(
            concept=self.item2,
            registrationAuthority=self.item1,
            registrationDate=timezone.now(),
            state=MDR.STATES.standard
        )

    def get_page(self, item):
        return item.get_absolute_url()

    def test_view_all_ras(self):
        self.logout()
        response = self.client.get(reverse('aristotle:all_registration_authorities'))
        self.assertEqual(response.status_code, 200)
