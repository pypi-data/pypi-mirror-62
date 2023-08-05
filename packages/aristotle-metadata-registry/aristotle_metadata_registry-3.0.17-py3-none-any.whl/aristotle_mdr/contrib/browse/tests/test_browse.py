from django.urls import reverse
from django.test import TestCase, tag

from aristotle_mdr import models

from aristotle_mdr.tests import utils


class TestBrowsePages(TestCase):
    def test_browse_pages_load(self):
        response = self.client.get(reverse('browse_apps'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('browse_models', args=['aristotle_mdr']))
        self.assertEqual(response.status_code, 200)

    def test_invalid_browse_pages_do_not_load(self):
        response = self.client.get(reverse('browse_apps'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('browse_concepts', args=['aristotle_mdr', 'workgroup']))
        self.assertEqual(response.status_code, 404)
        response = self.client.get(reverse('browse_concepts', args=['aristotle_mdr', 'registrationauthority']))
        self.assertEqual(response.status_code, 404)


class LoggedInViewConceptBrowsePages(utils.LoggedInViewPages):
    defaults = {}

    def setUp(self):
        super().setUp()

        self.item1 = self.itemType.objects.create(name="Test Item 1 (visible to tested viewers)",definition="my definition",workgroup=self.wg1,**self.defaults)
        self.item2 = self.itemType.objects.create(name="Test Item 2 (NOT visible to tested viewers)",definition="my definition",workgroup=self.wg2,**self.defaults)
        self.item3 = self.itemType.objects.create(name="Test Item 3 (visible to tested viewers)",definition="my definition",workgroup=self.wg1,**self.defaults)

        # Item 3 and 4 need to have a shared string in their name for `test_editor_can_view_browse_with_filters`
        # So, the character `3` *must* be in the name below!
        self.item4 = self.itemType.objects.create(name="Test Item 4 also like item 3 (visible to tested viewers)",definition="my definition",workgroup=self.wg1,**self.defaults)

        self.ra.register(self.item4,self.ra.public_state,self.su)

    def check_user_can_view_browse(self):
        response = self.client.get(
            reverse("browse_concepts",args=[self.itemType._meta.app_label,self.itemType._meta.model_name])
            )
        self.assertEqual(response.status_code,200)
        self.assertContains(response, self.item4.name)
        self.assertNotContains(response, self.item2.name)

    def test_anon_can_view_browse(self):
        self.logout()
        self.check_user_can_view_browse()

    @tag('registrar')
    def test_registrar_can_view_browse(self):
        # Make registrar a registrar of multiple ra's so that
        # ConceptQuerySet visible condition active
        ra2 = models.RegistrationAuthority.objects.create(
            name='Second RA',
            definition='Second',
            stewardship_organisation=self.steward_org_1
        )
        ra2.registrars.add(self.registrar)
        self.login_registrar()
        self.check_user_can_view_browse()

    def test_zero_item_should_not_show(self):
        self.logout()
        response = self.client.get(
            reverse("browse_concepts",args=[self.itemType._meta.app_label,self.itemType._meta.model_name])
            )

        self.assertEqual(response.status_code, 200)
        if(self.itemType.objects.all().count() == 0):
            self.assertNotContains(response, self.itemType._meta.model_name)
        else:
            self.assertContains(response, self.itemType._meta.model_name)

    def test_editor_can_view_browse(self):
        self.login_editor()
        response = self.client.get(
            reverse("browse_concepts",args=[self.itemType._meta.app_label,self.itemType._meta.model_name])
            )
        self.assertEqual(response.status_code,200)
        self.assertContains(response, self.item1.name)
        self.assertContains(response, self.item4.name)
        self.assertNotContains(response, self.item2.name)

    def test_itemtypes_with_no_items_dont_show_up(self):
        self.login_editor()

        response = self.client.get(reverse('browse_models', args=['aristotle_mdr']))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, self.itemType.get_verbose_name_plural())
        self.assertContains(response,
            reverse("browse_concepts",args=[self.itemType._meta.app_label,self.itemType._meta.model_name]),
        )

        self.item1.delete() #/browse/aristotle_mdr/objectclass
        self.item3.delete()
        self.item4.delete()

        response = self.client.get(reverse('browse_models', args=['aristotle_mdr']))
        self.assertEqual(response.status_code, 200)

        # self.assertNotContains(response, self.itemType.get_verbose_name_plural())
        self.assertNotContains(response,
            reverse("browse_concepts",args=[self.itemType._meta.app_label,self.itemType._meta.model_name]),
        )


class ObjectClassViewPage(LoggedInViewConceptBrowsePages,TestCase):
    url_name='objectClass'
    itemType=models.ObjectClass
class PropertyViewPage(LoggedInViewConceptBrowsePages,TestCase):
    url_name='property'
    itemType=models.Property
class UnitOfMeasureViewPage(LoggedInViewConceptBrowsePages,TestCase):
    url_name='unitOfMeasure'
    itemType=models.UnitOfMeasure
class ValueDomainViewPage(LoggedInViewConceptBrowsePages,TestCase):
    url_name='valueDomain'
    itemType=models.ValueDomain

class ConceptualDomainViewPage(LoggedInViewConceptBrowsePages,TestCase):
    url_name='conceptualDomain'
    itemType=models.ConceptualDomain
class DataElementConceptViewPage(LoggedInViewConceptBrowsePages,TestCase):
    url_name='dataElementConcept'
    itemType=models.DataElementConcept
class DataElementViewPage(LoggedInViewConceptBrowsePages,TestCase):
    url_name='dataElement'
    itemType=models.DataElement

    def test_template_overriden(self):
        """
        see file tests/apps/extension_test/templates/aristotle_mdr_browse/aristotle_mdr/dataelement_list.html
        """
        check_text = "This is a customised browse list of data elements"
        response = self.client.get(
            reverse("browse_concepts",args=[self.itemType._meta.app_label,self.itemType._meta.model_name])
        )
        self.assertContains(response, check_text)

class DataElementDerivationViewPage(LoggedInViewConceptBrowsePages,TestCase):
    url_name='dataelementderivation'
    itemType=models.DataElementDerivation
