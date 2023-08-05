import aristotle_mdr.models as MDR
from aristotle_mdr.models import _concept
import aristotle_mdr.tests.utils as utils

from django.test import TestCase, override_settings
from django.urls import reverse
from django.conf import settings

import reversion
from reversion.models import Version


class ComparatorTester(utils.LoggedInViewPages, TestCase):
    def setUp(self):
        super().setUp()
        self.steward_org_1 = MDR.StewardOrganisation.objects.create(name="Test SO")
        self.ra = MDR.RegistrationAuthority.objects.create(name="Test RA", stewardship_organisation=self.steward_org_1)
        self.wg = MDR.Workgroup.objects.create(name="Setup WG", stewardship_organisation=self.steward_org_1)

    def build_compare_url(self, a: _concept, b: _concept) -> str:
        query_params = f'?item_a={a.pk}&item_b={b.pk}'
        return reverse('aristotle:compare_concepts') + query_params

    def test_compare_with_no_selections_shows_please_select_item_prompt(self):
        """Test that when the compare page has no selections a prompt is given"""
        self.login_superuser()  # We don't need to worry about permissions here
        response = self.client.get(reverse('aristotle:compare_concepts'))
        self.assertResponseStatusCodeEqual(response=response, code=200)
        self.assertEqual(response.context['not_all_versions_selected'], True)

    def test_user_can_compare_different_dss_objects(self):
        """Test that when a user compares two different data elements within a DSS the difference is displayed"""
        # Create two different Data Elements
        data_element_1 = MDR.DataElement.objects.create(name="Data Element 1",
                                                        definition="My first Data Element",
                                                        submitter=self.editor,
                                                        )
        data_element_2 = MDR.DataElement.objects.create(name="Data Element 2",
                                                        definition="My second Data Element",
                                                        submitter=self.editor)
        aristotle_settings = settings.ARISTOTLE_SETTINGS
        aristotle_settings['CONTENT_EXTENSIONS'].append('aristotle_dse')
        aristotle_settings['CONTENT_EXTENSIONS'].append('comet')
        with override_settings(ARISTOTLE_SETTINGS=aristotle_settings):
            import aristotle_dse.models as DSE

            data_set_specification_1 = DSE.DataSetSpecification.objects.create(name="Data Set Specification 1",
                                                                               definition='',
                                                                               submitter=self.editor,
                                                                               )
            data_set_specification_2 = DSE.DataSetSpecification.objects.create(name='Data Set Specification 2',
                                                                               definition='',
                                                                               submitter=self.editor,
                                                                               )
            DSE.DSSDEInclusion.objects.create(dss=data_set_specification_1,
                                              data_element=data_element_1,
                                              reference='first')
            DSE.DSSDEInclusion.objects.create(dss=data_set_specification_2,
                                              data_element=data_element_2,
                                              reference='second')

            with reversion.revisions.create_revision():
                # Create versions for comparision
                data_set_specification_1.save()
                data_set_specification_2.save()

            data_element_1.refresh_from_db()
            data_element_2.refresh_from_db()
            self.assertEqual(data_element_1.name, 'Data Element 1')
            self.assertEqual(data_element_2.name, 'Data Element 2')
            self.assertEqual(Version.objects.get_for_object(data_set_specification_1).count(), 1)
            self.assertEqual(Version.objects.get_for_object(data_set_specification_2).count(), 1)

            self.login_superuser()  # We're not testing permissions
            response = self.client.get(self.build_compare_url(data_set_specification_1, data_set_specification_2))

            self.assertResponseStatusCodeEqual(response=response, code=200)
            self.assertContainsHtml(response, 'first')
            self.assertContainsHtml(response, 'second')

    def test_user_can_compare_different_distribution_objects(self):
        """Test that a user can compare differences between two different distributions"""
        data_element_1 = MDR.DataElement.objects.create(name="Data Element 1",
                                                        definition='',
                                                        submitter=self.editor)
        data_element_2 = MDR.DataElement.objects.create(name="Data Element 2",
                                                        definition='',
                                                        submitter=self.editor)
        aristotle_settings = settings.ARISTOTLE_SETTINGS
        aristotle_settings['CONTENT_EXTENSIONS'].append('aristotle_dse')
        aristotle_settings['CONTENT_EXTENSIONS'].append('comet')
        with override_settings(ARISTOTLE_SETTINGS=aristotle_settings):
            import aristotle_dse.models as DSE
            distribution_1 = DSE.Distribution.objects.create(
                name='Distribution 1',
                definition='',
                submitter=self.editor)
            distribution_2 = DSE.Distribution.objects.create(name='Distribution 2',
                                                             definition='',
                                                             submitter=self.editor)
            DSE.DistributionDataElementPath.objects.create(distribution=distribution_1,
                                                           data_element=data_element_1,
                                                           logical_path="first")
            DSE.DistributionDataElementPath.objects.create(distribution=distribution_2,
                                                           data_element=data_element_2,
                                                           logical_path='second')
            with reversion.revisions.create_revision():
                distribution_1.save()
                distribution_2.save()

            self.login_superuser()
            response = self.client.get(self.build_compare_url(distribution_1, distribution_2))

            self.assertResponseStatusCodeEqual(response=response, code=200)
            self.assertContainsHtml(response, 'first')
            self.assertContainsHtml(response, 'second')
