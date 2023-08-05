from django.test import TestCase, override_settings
from django.utils import timezone
from django.urls import reverse
from django.conf import settings

import aristotle_mdr.models as MDR
import aristotle_dse.models as DSE
from aristotle_mdr.tests import utils
from aristotle_mdr.contrib.publishing.models import VersionPermissions
from aristotle_mdr.contrib.custom_fields.models import CustomField, CustomValue
from aristotle_mdr.constants import visibility_permission_choices as VISIBILITY_PERMISSION_CHOICES

import datetime
import reversion
from reversion.models import Version


class VersionComparisionTestCase(utils.AristotleTestUtils, TestCase):
    """Class to test the version comparision view"""

    def setUp(self):
        super().setUp()

        self.object_class = MDR.ObjectClass.objects.create(
            name='Object Class',
            definition='description',
            submitter=self.editor,
            workgroup=self.wg1,
        )

        self.data_element = MDR.DataElement.objects.create(
            name="Data Element",
            definition="definition",
            submitter=self.editor,
            workgroup=self.wg1

        )

        self.so = MDR.StewardOrganisation.objects.create(
            name='Best Stewardship Organisation',
        )

        self.ra = MDR.RegistrationAuthority.objects.create(
            name='First RA',
            definition='First',
            stewardship_organisation=self.so
        )

        self.custom_field = CustomField.objects.create(
            order=0,
            name='Bad Word',
            type='str',
            help_text='A real bad word'
        )

        self.html_custom_field = CustomField.objects.create(
            order=1,
            name='Very Bad Word',
            type='html',
            help_text='An extremely bad word'
        )

        self.data_element = MDR.DataElement.objects.create(
            name="test name",
            definition="test definition",
        )

        aristotle_settings = settings.ARISTOTLE_SETTINGS
        aristotle_settings['CONTENT_EXTENSIONS'].append('aristotle_dse')
        aristotle_settings['CONTENT_EXTENSIONS'].append('comet')
        with override_settings(ARISTOTLE_SETTINGS=aristotle_settings):
            from comet.models import Indicator, IndicatorNumeratorDefinition

            self.data_set_specification = DSE.DataSetSpecification.objects.create(
                name='Data Set Specification',
                definition='definition',
                submitter=self.editor,
                workgroup=self.wg1
            )

            self.indicator = Indicator.objects.create(
                name='indicator',
                definition='indicator',
            )
            # Add a numerator
            IndicatorNumeratorDefinition.objects.create(
                data_element=self.data_element,
                indicator=self.indicator,
                order=1
            )

    def create_two_versions(self, concept):
        with reversion.revisions.create_revision():
            concept.name = "Older Version of a Concept"
            concept.save()

        with reversion.revisions.create_revision():
            concept.name = "Newer Version of a Concept"
            concept.save()

        versions = Version.objects.get_for_object(concept)
        self.assertEqual(versions.count(), 2)

    def test_altered_on_concept_field_displayed(self):
        """Test that field that is **on** the concept, and has
        had content altered between the saves is displayed in the compare versions view"""
        self.login_viewer()

        self.create_two_versions(self.object_class)

        # Go to the view
        versions = Version.objects.get_for_object(self.object_class)
        url = reverse('aristotle:compare_versions', args=[self.data_set_specification.id])
        query_url = url + '?v1={}&v2={}'.format(versions[0].id, versions[1].id)

        response = self.client.get(query_url)

        # Check that the response contains 'Name'
        self.assertContainsHtml(response, 'Name')

    def test_added_subitem_displayed(self):
        """Test that a subitem (ex. custom fields) added to a concept between versions is displayed """
        self.login_viewer()

        # Create and attach a CustomValue to the Object Class

        with reversion.revisions.create_revision():
            # Don't really need to do anything here, just need a version
            self.object_class.save()

        with reversion.revisions.create_revision():
            CustomValue.objects.create(
                field=self.custom_field,
                concept=self.object_class,
                content="Freshly created and served"
            )
            self.object_class.save()

        versions = Version.objects.get_for_object(self.object_class)
        self.assertEqual(versions.count(), 2)

        # Compare the versions
        url = reverse('aristotle:compare_versions', args=[self.object_class.id])
        query_url = url + '?v1={}&v2={}'.format(versions[0].id, versions[1].id)

        response = self.client.get(query_url)
        self.assertEqual(response.status_code, 200)

        self.assertContainsHtml(response, 'Freshly created and served')

    def test_removed_subitem_displayed(self):
        """Test that a subitem (ex. custom fields) removed from a concept between versions is displayed"""
        self.login_viewer()

        # Create and attach a CustomValue to the Object Class
        custom_value = CustomValue.objects.create(
            field=self.custom_field,
            concept=self.object_class,
            content='Heck'
        )

        with reversion.revisions.create_revision():
            custom_value.content = 'More Heck'
            custom_value.save()
            self.object_class.save()

        with reversion.revisions.create_revision():
            custom_value.delete()
            self.object_class.save()

        versions = Version.objects.get_for_object(self.object_class)
        self.assertEqual(versions.count(), 2)

        # Compare the versions
        url = reverse('aristotle:compare_versions', args=[self.object_class.id])
        query_url = url + '?v1={}&v2={}'.format(versions[0].id, versions[1].id)

        response = self.client.get(query_url)
        self.assertEqual(response.status_code, 200)

        self.assertContainsHtml(response, 'Bad Word')

    def test_changed_subitem_displayed(self):
        """Test that a subitem (ex. custom fields) that has had content on it altered is displayed """
        self.login_viewer()

        # Create and attach a CustomValue to the Object Class
        custom_value = CustomValue.objects.create(
            field=self.custom_field,
            concept=self.object_class,
            content='Heck'
        )

        with reversion.revisions.create_revision():
            custom_value.content = 'More Heck'
            custom_value.save()
            self.object_class.save()

        with reversion.revisions.create_revision():
            custom_value.content = 'Even More Heck'
            custom_value.save()
            self.object_class.save()

        versions = Version.objects.get_for_object(self.object_class)
        self.assertEqual(versions.count(), 2)

        # Compare the versions
        url = reverse('aristotle:compare_versions', args=[self.object_class.id])
        query_url = url + '?v1={}&v2={}'.format(versions[1].id, versions[0].id)

        response = self.client.get(query_url)
        self.assertEqual(response.status_code, 200)

        self.assertContainsHtml(response, 'Bad Word')

    def test_version_compare_chronology_correct(self):
        """Test that the versions are compared with the correct chronology. We want the earlier item to be version 1
        and the older item to be version 2"""
        self.login_viewer()

        # Create two versions of an Object Class
        self.create_two_versions(self.object_class)

        # Confirm that two versions were created
        versions = reversion.models.Version.objects.get_for_object(self.object_class)

        # Build query in the wrong order
        url = reverse('aristotle:compare_versions', args=[self.object_class.id])
        query_url = url + '?v1={}&v2={}'.format(versions[1].id, versions[0].id)

        # Assert that they have been correctly rearranged
        response = self.client.get(query_url)
        self.assertEqual(response.status_code, 200)

        # -1 is a delete, 1 is an insert
        failure_message = 'Older item should be deleted, newer item should be added'

        deleted_tuple = (-1, 'Old')
        self.assertTrue(str(deleted_tuple) in str(response.context), msg=failure_message)

        # Should be the same when we reverse the query
        query_url = url + '?v1={}&v2={}'.format(versions[0].id, versions[1].id)
        response = self.client.get(query_url)

        self.assertTrue(str(deleted_tuple) in str(response.context), msg=failure_message)

    def test_html_fields_of_custom_values_detected_as_html_fields(self):
        """Test that the HTML fields of custom values are correctly detected as HTML fields. A test is written
        for this because CustomFields store HTML fields as TextFields so we have custom logic to handle this"""
        self.login_viewer()

        # Create and attach a CustomValue to the Object Class
        custom_value = CustomValue.objects.create(
            field=self.html_custom_field,
            concept=self.object_class,
            content='<em>HECK</em>'
        )
        # Create two versions of this CustomValue
        with reversion.revisions.create_revision():
            custom_value.content = '<b>HECK</b>'
            custom_value.save()
            self.object_class.save()

        with reversion.revisions.create_revision():
            custom_value.content = '<i>heck</i>'
            custom_value.save()
            self.object_class.save()

        # Assert that only two versions were created
        versions = Version.objects.get_for_object(self.object_class)
        self.assertEqual(versions.count(), 2)

        url = reverse('aristotle:compare_versions', args=[self.object_class.id])
        query = url + '?v1={}&v2={}'.format(versions[0].id, versions[1].id)

        response = self.client.get(query)
        self.assertEqual(response.status_code, 200)

        diffs = response.context['diffs']
        self.assertEqual(diffs['customvalue_set']['diffs'][0]['content']['is_html'], True)

    def test_compare_view_403s_when_viewer_doesnt_have_permission_to_view_both_versions(self):
        """Test that the compare view 403s when the viewer doesn't have permission to view both versions """
        # Login in a regular user
        self.login_regular_user()

        # Create two versions
        with reversion.revisions.create_revision():
            self.object_class.name = 'An older Object Class'
            self.object_class.save()

        with reversion.revisions.create_revision():
            self.object_class.name = ' A newer Object Class'
            self.object_class.save()

        # Assert that only two versions were created
        self.assertEqual(Version.objects.get_for_object(self.object_class).count(), 2)

        # Create VersionPermission objects for the two versions
        versions = Version.objects.get_for_object(self.object_class)

        VersionPermissions.objects.create(version=versions[0],
                                          visibility=VISIBILITY_PERMISSION_CHOICES.public)

        VersionPermissions.objects.create(version=versions[1],
                                          visibility=VISIBILITY_PERMISSION_CHOICES.workgroup)

        # Register the ObjectClass as public, but not the versions
        self.status = MDR.Status.objects.create(
            concept=self.object_class,
            registrationAuthority=self.ra,
            registrationDate=timezone.now(),
            state=self.ra.public_state
        )

        # Assert that the CompareVersions view 403s
        url = reverse('aristotle:compare_fields', args=[self.data_set_specification.id])
        query_url = url + '?v1={}&v2={}'.format(versions[0].id, versions[1].id)

        response = self.client.get(query_url)

        self.assertEqual(response.status_code, 403)

    def test_view_rendered_html_field_for_subitem(self):
        """Test that the CompareFieldsHTMLView renders the value of a subitem's HTML field. Using the definition
         of a DSS Grouping as a indicative value"""

        self.login_viewer()
        # Create two versions with DSSGroupings
        with reversion.revisions.create_revision():
            dss_grouping = DSE.DSSGrouping.objects.create(
                dss=self.data_set_specification,
                name='Grouping',
                definition='This is a DSS Grouping')

            self.data_set_specification.save()

        with reversion.revisions.create_revision():
            dss_grouping.definition = 'This is an updated DSS Grouping'
            dss_grouping.save()
            self.data_set_specification.save()

        # Confirm that two versions were created
        versions = reversion.models.Version.objects.get_for_object(self.data_set_specification)
        self.assertEqual(versions.count(), 2)

        # Build the get query parameter. Format is parent_field.{{ number of subitem indexed from 0}}.field
        url = reverse('aristotle:compare_fields', args=[self.data_set_specification.id])
        query = url + '?v1={}&v2={}&field=groups.0.definition'.format(versions[0].id, versions[1].id)

        response = self.client.get(query)
        self.assertEqual(response.status_code, 200)

        # Check the content of the fields
        self.assertEqual(response.context['html_fields'], ['This is an updated DSS Grouping', 'This is a DSS Grouping'])

    def test_all_added_data_elements_appear_in_comparision_view(self):
        self.login_viewer()

        with reversion.revisions.create_revision():
            self.name = "New Data Set Specification"
            self.data_set_specification.save()

        with reversion.revisions.create_revision():
            # Create 4 DSS Data Elements
            DSE.DSSDEInclusion.objects.create(
                data_element=self.data_element,
                reference="Hello",
                conditional_inclusion="Test Obligation",
                order=0,
                dss=self.data_set_specification
            )
            DSE.DSSDEInclusion.objects.create(
                data_element=self.data_element,
                reference="Hola",
                conditional_inclusion="Test Obligation",
                order=0,
                dss=self.data_set_specification
            )
            DSE.DSSDEInclusion.objects.create(
                data_element=self.data_element,
                reference="Hallo",
                conditional_inclusion="Test Obligation",
                order=0,
                dss=self.data_set_specification
            )
            DSE.DSSDEInclusion.objects.create(
                data_element=self.data_element,
                reference="Hoi",
                conditional_inclusion="Test Obligation",
                order=0,
                dss=self.data_set_specification
            )
            self.data_set_specification.name = "Updated DSS"
            self.data_set_specification.save()

        # Confirm that two versions were created
        versions = reversion.models.Version.objects.get_for_object(self.data_set_specification)
        self.assertEqual(versions.count(), 2)

        # Build the get query parameter. Format is parent_field.{{ number of subitem indexed from 0}}.field
        url = reverse('aristotle:compare_versions', args=[self.data_set_specification.id])
        query = url + '?v1={}&v2={}'.format(versions[0].id, versions[1].id)

        response = self.client.get(query)
        self.assertEqual(response.status_code, 200)

        # Assert that all the versions are showing up
        self.assertContainsHtml(response, 'Hello')
        self.assertContainsHtml(response, 'Hola')
        self.assertContainsHtml(response, 'Hallo')
        self.assertContainsHtml(response, 'Hoi')

    def test_indicator_with_incomplete_numerator_doesnt_500(self):
        self.login_superuser()
        with reversion.revisions.create_revision():
            self.indicator.definition = "New indicator"
            self.indicator.save()

        # Make a minor modification to the definition
        with reversion.revisions.create_revision():
            self.indicator.definition = "New indicator"
            self.indicator.save()

        # Confirm that two versions were created
        versions = reversion.models.Version.objects.get_for_object(self.indicator)
        self.assertEqual(versions.count(), 2)

        # Build the get query parameter. Format is parent_field.{{ number of subitem indexed from 0}}.field
        url = reverse('aristotle:compare_versions', args=[self.indicator.id])
        query = url + '?v1={}&v2={}'.format(versions[0].id, versions[1].id)

        response = self.client.get(query)

        # Confirm that the page loads successfully
        self.assertEqual(response.status_code, 200)


class TestViewingVersionPermissions(utils.AristotleTestUtils, TestCase):
    """ Class to test the version permissions  """

    def setUp(self):
        super().setUp()

        # Create a new item without version permissions
        with reversion.revisions.create_revision():
            self.reversion_item_without_permissions = MDR.ObjectClass.objects.create(
                name="A concept without permissions",
                definition="Concept with no permissions",
                submitter=self.editor,
                workgroup=self.wg1
            )
            reversion.revisions.set_comment("First edit")

        self.version_without_permission = Version.objects.get_for_object(
            self.reversion_item_without_permissions).first()

        # Item with workgroup version permissions
        with reversion.revisions.create_revision():
            self.reversion_item_with_workgroup_permission = MDR.ObjectClass.objects.create(
                name="A published item",
                definition="Concept with no permissions",
                submitter=self.editor,
                workgroup=self.wg1
            )

        self.version_with_workgroup_permission = Version.objects.get_for_object(
            self.reversion_item_with_workgroup_permission).first()

        VersionPermissions.objects.create(version=self.version_with_workgroup_permission,
                                          visibility=VISIBILITY_PERMISSION_CHOICES.workgroup)

        # Item with authenticated user version permissions
        with reversion.revisions.create_revision():
            self.reversion_item_with_authenticated_user_permissions = MDR.ObjectClass.objects.create(
                name='A item for authenticated users only',
                definition="Authenticated user permission",
                submitter=self.editor,
                workgroup=self.wg1
            )
        self.version_with_auth_user_permission = Version.objects.get_for_object(
            self.reversion_item_with_authenticated_user_permissions).first()

        VersionPermissions.objects.create(version=self.version_with_auth_user_permission,
                                          visibility=VISIBILITY_PERMISSION_CHOICES.auth)

        # Item with public version permissions
        with reversion.revisions.create_revision():
            self.reversion_item_with_public_permissions = MDR.ObjectClass.objects.create(
                name='A item for authenticated users only',
                definition="Authenticated user permission",
                submitter=self.editor,
                workgroup=self.wg1)

        self.version_with_public_user_permission = Version.objects.get_for_object(
            self.reversion_item_with_public_permissions).first()

        VersionPermissions.objects.create(version=self.version_with_public_user_permission,
                                          visibility=VISIBILITY_PERMISSION_CHOICES.public)

    def test_superuser_can_view_version_with_no_permissions(self):
        """ Test that a superuser can view a version with no permission"""
        self.login_superuser()

        response = self.client.get(reverse('aristotle:item_history', args=[self.reversion_item_without_permissions.id]))
        self.assertEqual(len(response.context['versions']), 1)

    def test_user_in_workgroup_can_view_version_with_no_permissions(self):
        self.login_viewer()

        response = self.client.get(reverse('aristotle:item_history', args=[self.reversion_item_without_permissions.id]))
        self.assertEqual(len(response.context['versions']), 1)

    def test_user_not_in_workgroup_cant_view_version_with_no_permissions(self):
        self.login_regular_user()  # Regular user is not in workgroup

        with reversion.revisions.create_revision():
            item_without_permissions = MDR.ObjectClass.objects.create(
                name="A concept without permissions",
                definition="Concept with no permissions",
                submitter=self.editor,
                workgroup=self.wg1
            )
            reversion.revisions.set_comment("First edit")

        self.so = MDR.StewardOrganisation.objects.create(
            name='Best Stewardship Organisation',
        )

        self.ra = MDR.RegistrationAuthority.objects.create(
            name='First RA',
            definition='First',
            stewardship_organisation=self.so
        )
        # Register the ObjectClass as public, but not the version
        self.status = MDR.Status.objects.create(
            concept=item_without_permissions,
            registrationAuthority=self.ra,
            registrationDate=timezone.now(),
            state=self.ra.public_state
        )

        response = self.client.get(reverse('aristotle:item_history', args=[item_without_permissions.id]))
        self.assertEqual((len(response.context['versions'])), 0)

    def test_user_can_see_own_version_if_item_still_in_sandbox(self):
        self.login_regular_user()

        with reversion.revisions.create_revision():
            sandbox_item = MDR.ObjectClass.objects.create(
                name="A published item",
                definition="Concept with no permissions",
                submitter=self.regular)

        response = self.client.get(reverse('aristotle:item_history', args=[sandbox_item.id]))
        self.assertEqual((len(response.context['versions'])), 1)

    def test_change_author_displayed_in_versions(self):
        """Test that the author that made the change is displayed in the List Versions view"""
        self.login_superuser()

        item = MDR.ObjectClass.objects.create(
            name="An item",
            definition="This is an object class",
            submitter=self.regular
        )
        with reversion.revisions.create_revision():
            item.name = 'An edited item'
            reversion.revisions.set_user(self.su)
            item.save()

        response = self.client.get(reverse('aristotle:item_history', args=[item.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContainsHtml(response, 'super@example.com')

    def test_change_comment_displayed_in_version(self):
        """Test that a supplied change comment is displayed in the List Versions view"""
        self.login_superuser()

        # Create an item
        item = MDR.ObjectClass.objects.create(
            name="A new item",
            definition="This really is an object class",
            submitter=self.regular
        )

        # Edit the item, provide a change comment
        with reversion.revisions.create_revision():
            item.name = "This is item is so different now"
            item.save()
            reversion.revisions.set_comment("I don't have to tell you why I changed this")

        # Check that it appears in the item history page
        response = self.client.get(reverse('aristotle:item_history', args=[item.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContainsHtml(response, "I don&#39;t have to tell you why I changed this")


class CreationOfVersionTests(utils.AristotleTestUtils, TestCase):
    def test_newly_created_version_permissions_default_to_workgroup(self):
        """Integration test to check that when an item is edited:
           1) A version is created
           2) That an associated VersionPermission is created with the permission defaulting to workgroup"""
        # ///Arrange

        self.login_editor()

        object_class = MDR.ObjectClass.objects.create(
            name="A published item",
            definition="I wonder what the version permission for this is",
            submitter=self.editor
        )
        # ///Act

        # Load the EditItem page
        response = self.client.get(reverse('aristotle:edit_item', args=[object_class.id]))
        self.assertEqual(response.status_code, 200)

        # Edit the item
        updated_item = utils.model_to_dict_with_change_time(response.context['item'])
        updated_name = updated_item['name'] + " updated!"
        updated_item['name'] = updated_name
        change_comment = "I changed this because I can"
        updated_item['change_comments'] = change_comment
        response = self.client.post(reverse('aristotle:edit_item', args=[object_class.id]), updated_item)

        # Decache
        object_class = MDR.ObjectClass.objects.get(pk=object_class.pk)

        # ///Assert
        self.assertEqual(object_class.name, updated_name)

        # Load the version
        version = Version.objects.get_for_object(object_class).first()

        # Load the associated VersionPermission object
        version_permission = VersionPermissions.objects.get_object_or_none(version=version)

        # Check that it defaults to 2
        self.assertEqual(version_permission.visibility, VISIBILITY_PERMISSION_CHOICES.workgroup)


class CheckStatusHistoryReversionTests(utils.AristotleTestUtils, TestCase):
    def setUp(self):
        super().setUp()

        self.object_class = MDR.ObjectClass.objects.create(
            name="A published item",
            definition="I wonder what the version permission for this is",
            submitter=self.editor,
        )

        with reversion.revisions.create_revision():
            self.status = MDR.Status.objects.create(
                concept=self.object_class,
                registrationAuthority=self.ra,
                registrationDate=datetime.date(2000, 1, 1),
            )

    def test_statuses_reversion_page_works(self):
        self.login_superuser()

        # Load the Reversions page for Statuses
        response = self.client.get(
            reverse('aristotle:statusHistory', args=[self.status.id, self.object_class.id, self.ra.id]))
        self.assertEqual(response.status_code, 200)

    def test_status_edit_page_is_restricted_to_superusers(self):
        """Test that the status edit page 403s for any user but superusers"""
        self.logout()
        url = reverse('friendly_login') + '?next=' + reverse('aristotle:editStatus', args=[self.status.id,
                                                                                           self.object_class.id,
                                                                                           self.ra.id])
        response = self.client.get(
            reverse('aristotle:editStatus', args=[self.status.id, self.object_class.id, self.ra.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, url)

        self.login_viewer()
        response = self.client.get(
            reverse('aristotle:editStatus', args=[self.status.id, self.object_class.id, self.ra.id]))
        self.assertEqual(response.status_code, 403)

        self.login_regular_user()
        response = self.client.get(
            reverse('aristotle:editStatus', args=[self.status.id, self.object_class.id, self.ra.id]))
        self.assertEqual(response.status_code, 403)
        self.logout()

        self.login_editor()
        response = self.client.get(
            reverse('aristotle:editStatus', args=[self.status.id, self.object_class.id, self.ra.id]))
        self.assertEqual(response.status_code, 403)
        self.logout()

        self.login_superuser()
        response = self.client.get(
            reverse('aristotle:editStatus', args=[self.status.id, self.object_class.id, self.ra.id]))
        self.assertEqual(response.status_code, 200)
        self.logout()

    def test_status_delete_page_is_restricted_to_superusers(self):
        """Test that the status edit page 403s for any user but superusers"""
        self.logout()
        url = reverse('friendly_login') + '?next=' + reverse('aristotle:deleteStatus', args=[self.status.id,
                                                                                             self.object_class.id])
        response = self.client.get(
            reverse('aristotle:deleteStatus', args=[self.status.id, self.object_class.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, url)

        self.login_viewer()
        response = self.client.get(
            reverse('aristotle:deleteStatus', args=[self.status.id, self.object_class.id]))
        self.assertEqual(response.status_code, 403)

        self.login_regular_user()
        response = self.client.get(
            reverse('aristotle:deleteStatus', args=[self.status.id, self.object_class.id]))
        self.assertEqual(response.status_code, 403)
        self.logout()

        self.login_editor()
        response = self.client.get(
            reverse('aristotle:deleteStatus', args=[self.status.id, self.object_class.id]))
        self.assertEqual(response.status_code, 403)
        self.logout()

        self.login_superuser()
        response = self.client.get(
            reverse('aristotle:deleteStatus', args=[self.status.id, self.object_class.id]))
        self.assertEqual(response.status_code, 200)
        self.logout()

    def test_statuses_reversions_list_only_includes_the_first_reversion_object(self):
        self.login_superuser()

        response = self.client.get(
            reverse('aristotle:statusHistory', args=[self.status.id, self.object_class.id, self.ra.id]))

        self.assertEqual(len(response.context['versions']), 1)

    def test_statuses_reversions_list_is_populated_after_creating_reversion(self):
        self.login_superuser()

        with reversion.revisions.create_revision():
            MDR.Status.objects.create(
                concept=self.object_class,
                registrationAuthority=self.ra,
                changeDetails="My new details",
                state=MDR.STATES.candidate,
                registrationDate=datetime.date(2000, 1,1)
            )
            reversion.revisions.set_comment("This is an edit")

        response = self.client.get(
            reverse('aristotle:statusHistory', args=[self.status.id, self.object_class.id, self.ra.id])
        )

        self.assertEqual(len(response.context['versions']), 1)

    def test_status_reversion_page_only_visible_to_superusers(self):
        """Test that the status reversion page 403s for any user but superusers"""
        self.logout()
        url = reverse('friendly_login') + '?next=' + reverse('aristotle:statusHistory', args=[self.status.id,
                                                                                              self.object_class.id,
                                                                                              self.ra.id])
        response = self.client.get(
            reverse('aristotle:statusHistory', args=[self.status.id, self.object_class.id, self.ra.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, url)

        self.login_viewer()
        response = self.client.get(
            reverse('aristotle:statusHistory', args=[self.status.id, self.object_class.id, self.ra.id]))
        self.assertEqual(response.status_code, self.Status.FORBIDDEN)

        self.login_regular_user()
        response = self.client.get(
            reverse('aristotle:statusHistory', args=[self.status.id, self.object_class.id, self.ra.id]))
        self.assertEqual(response.status_code, self.Status.FORBIDDEN)
        self.logout()

        self.login_editor()
        response = self.client.get(
            reverse('aristotle:statusHistory', args=[self.status.id, self.object_class.id, self.ra.id]))
        self.assertEqual(response.status_code, self.Status.FORBIDDEN)
        self.logout()

        self.login_superuser()
        response = self.client.get(
            reverse('aristotle:statusHistory', args=[self.status.id, self.object_class.id, self.ra.id]))
        self.assertEqual(response.status_code, self.Status.OK)
        self.logout()


class TestStatusViews(utils.AristotleTestUtils, TestCase):
    def test_status_history_displays_all_reversions(self):
        """Test that status reversions are displayed correctly"""
        self.login_superuser()
        object_class = MDR.ObjectClass.objects.create(name="Object Class",
                                                      definition="Object Class",
                                                      submitter=self.editor)
        status = MDR.Status.objects.create(
            concept=object_class,
            registrationAuthority=self.ra,
            registrationDate=datetime.date(2000, 1, 1),
            changeDetails=f"Registered"
        )
        for i in range(1, 6):
            with reversion.create_revision():
                status.registrationDate = datetime.date(2000 + i, 1, 1)
                status.save()

        response = self.client.get(
            reverse('aristotle:statusHistory', args=[status.id, object_class.id, self.ra.id])
        )
        self.assertEqual(response.status_code, self.Status.OK)

        versions = response.context['versions']
        self.assertEqual(versions.count(), 5)

    def test_status_history_handles_no_reversion_history(self):
        """Not all statuses will have a reversion, make sure the view doesn't fail if there are no status histories"""
        self.login_superuser()
        # Create an object class
        object_class = MDR.ObjectClass.objects.create(name="Object Class",
                                                      definition="Object Class",
                                                      submitter=self.editor)
        # Register it without creating a reversion
        status = MDR.Status.objects.create(
            concept=object_class,
            registrationAuthority=self.ra,
            registrationDate=datetime.date(2000, 1, 1)
        )
        response = self.client.get(
            reverse('aristotle:statusHistory', args=[status.id, object_class.id, self.ra.id])
        )
        self.assertEqual(response.status_code, self.Status.OK)
        self.assertContains(response, "No history for")

    def test_fields_are_set_correctly_when_editing_status(self):
        """Test that the EditStatus view correctly sets fields when editing a status"""
        self.login_superuser()

        # Create an object class
        object_class = MDR.ObjectClass.objects.create(name="Object Class",
                                                      definition="Object Class",
                                                      submitter=self.editor)
        status = MDR.Status.objects.create(
            concept=object_class,
            registrationAuthority=self.ra,
            registrationDate=datetime.date(2000, 1, 1)
        )
        data = {'state': 2,
                'changeDetails': "Endorsed by my METADATA REGISTRY",
                "registrationDate": datetime.date(2001, 1, 1)}

        response = self.client.post(
            reverse('aristotle:editStatus', args=[status.id, object_class.id, self.ra.id]),
            data
        )
        status.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(status.state, 2)
        self.assertEqual(status.changeDetails, "Endorsed by my METADATA REGISTRY")

        self.assertEqual(status.registrationDate, datetime.date(2001, 1, 1))

    def test_status_change_message_is_set_correctly(self):
        """Test that the change message in the reversion is set correctly"""
        self.login_superuser()

        # Create an object class
        object_class = MDR.ObjectClass.objects.create(name="Object",
                                                      definition="Object",
                                                      submitter=self.editor)

        status = MDR.Status.objects.create(
            concept=object_class,
            registrationAuthority=self.ra,
            registrationDate=datetime.date(2000, 1, 1)

        )
        data = {
            "state": 2,
            "registrationDate": datetime.date(2000, 1, 1),
            "changeDetails": "Endorsed by MY METADATA REGISTRY",
            "change_message": "I changed this because I slipped on my keyboard"
        }

        response = self.client.post(
            reverse("aristotle:editStatus", args=[status.id, object_class.id, self.ra.id]),
            data=data
        )
        self.assertEqual(response.status_code, 302)

        version = Version.objects.get_for_object(status).first()
        self.assertEqual(version.revision.comment, "I changed this because I slipped on my keyboard")

