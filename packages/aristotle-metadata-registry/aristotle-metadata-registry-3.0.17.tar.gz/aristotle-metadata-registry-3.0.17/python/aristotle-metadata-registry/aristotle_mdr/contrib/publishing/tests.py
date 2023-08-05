from aristotle_mdr import perms
from aristotle_mdr.constants import visibility_permission_choices
from aristotle_mdr.contrib.publishing import models as pub
from aristotle_mdr.forms.search import get_permission_sqs
from aristotle_mdr.models import ObjectClass, _concept, Measure
from aristotle_mdr.tests import utils

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.contrib.contenttypes.models import ContentType
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from reversion import revisions as reversion
import datetime
from datetime import timedelta
from unittest import skip


class TestPublishing(utils.AristotleTestUtils, TestCase):
    def setUp(self):
        super().setUp()
        self.submitting_user = get_user_model().objects.create_user(
            email="self@publisher.net",
            password="self-publisher"
        )

        with reversion.create_revision():
            self.item = ObjectClass.objects.create(
                name="A published item",
                definition="test",
                submitter=self.submitting_user
            )

    def tearDown(self):
        call_command('clear_index', interactive=False, verbosity=0)

    @skip("TODO: rethink stewardship organisation permissions")
    def test_publishing_item_with_workgroup_permissions_is_only_visible_to_workgroup_members(self):
        """Test that publishing an item with workgroup permissions is only visible to workgroup members"""
        self.login_superuser()

        # Create a Managed Item
        Measure.objects.create(name="Centimeters",
                               definition="The inferior form of meters",
                               stewardship_organisation=self.steward_org_1)

        pub.PublicationRecord.objects.create(
            content_type=ContentType.objects.get_for_model(_concept),
            object_id=self.item.pk,
            publisher=self.submitting_user,
            publication_date=timezone.now() - timedelta(days=2),
            permission=visibility_permission_choices.public
        )

    def test_publishing_item_via_form(self):
        """Test that a managed item can be created via the form"""
        self.login_superuser()  # Not testing permissions

        # Create a Managed Item
        measure = Measure.objects.create(name="Centimeters",
                                         definition="The inferior form of meters",
                                         stewardship_organisation=self.steward_org_1)

        # Go to the publish page
        response = self.client.get(
            reverse('aristotle_publishing:publish_item', args=[measure._meta.model_name, measure.id])
        )
        self.assertResponseStatusCodeEqual(response=response, code=200)
        data = {'permission': visibility_permission_choices.public,
                'publication_date': datetime.date(2000, 1, 1)}
        response = self.client.post(
            reverse('aristotle_publishing:publish_item', args=[measure._meta.model_name, measure.id]), data
        )
        self.assertResponseStatusCodeEqual(response=response, code=302)
        self.logout()
        # Check that the item is publicly accessible, because it has been published
        response = self.client.get(measure.get_absolute_url())
        self.assertResponseStatusCodeEqual(response=response, code=200)

    def test_publishing_item_in_future_does_not_make_it_immediately_visible(self):
        """Test that publishing an item in the future does not make it immediately visible"""
        self.login_superuser()  # Not testing permissions

        # Create a Managed Item
        measure = Measure.objects.create(name="Centimeters",
                                         definition="The inferior form of meters",
                                         stewardship_organisation=self.steward_org_1)
        response = self.client.get(
            reverse("aristotle_publishing:publish_item", args=[measure._meta.model_name, measure.id])
        )
        self.assertResponseStatusCodeEqual(response=response, code=200)
        data = {'permission': visibility_permission_choices.public,
                'publication_date': datetime.date.today() + timedelta(days=10)}  # Publish it 10 days in the future

        response = self.client.post(
            reverse('aristotle_publishing:publish_item', args=[measure._meta.model_name, measure.id]),
            data
        )
        self.assertResponseStatusCodeEqual(response=response, code=302)
        self.logout()
        response = self.client.get(measure.get_absolute_url())
        self.assertResponseStatusCodeEqual(response=response, code=403)
        # Confirm that we are prevented from seeing the Managed Item

    def test_self_publish_queryset_anon(self):
        """Check that publishing an item as 'Public' makes it visible to anonymous users"""
        self.logout()
        response = self.client.get(self.item.get_absolute_url())
        # self.assertTrue(response.status_code == 302)

        self.item = ObjectClass.objects.get(pk=self.item.pk)
        # self.assertFalse(self.item._is_public)

        psqs = get_permission_sqs()
        psqs = psqs.auto_query('published').apply_permission_checks()

        self.assertEqual(len(psqs), 0)

        pub.PublicationRecord.objects.create(
            content_type=ContentType.objects.get_for_model(_concept),
            object_id=self.item.pk,
            publisher=self.submitting_user,
            publication_date=timezone.now() - timedelta(days=2),
            permission=visibility_permission_choices.public
        )

        self.item = ObjectClass.objects.get(pk=self.item.pk)
        self.assertTrue(self.item.concept.publication_details.count() == 1)

        # TODO: Make the below true
        # self.assertTrue(self.item.publication_details.count() == 1)

        items = ObjectClass.objects.all().public().all()
        self.assertTrue(items.count() == 1)
        items = _concept.objects.all().public().all()
        self.assertTrue(items.count() == 1)
        ObjectClass.objects.public().get(pk=self.item.pk)
        self.assertTrue(self.item.can_view(AnonymousUser()))

        response = self.client.get(self.item.get_absolute_url())
        self.assertTrue(response.status_code == 200)

        self.item = ObjectClass.objects.get(pk=self.item.pk)

        psqs = get_permission_sqs()
        psqs = psqs.auto_query('published').apply_permission_checks()
        self.assertEqual(len(psqs), 1)

    def test_publish_button_visibility_no_perm(self):
        """Check that a user that cannot publish the item also can't see the button"""

        # Add item to so and wg
        self.item.stewardship_organisation = self.steward_org_1
        self.item.workgroup = self.wg1
        self.item.save()

        # Login as someone who can view the item but can not publish
        self.assertFalse(perms.user_can_publish_object(self.editor, self.item))

        self.login_editor()
        response = self.reverse_get(
            'aristotle:item',
            reverse_args=[self.item.id],
            follow=True
        )
        self.assertEqual(response.status_code, 200)

        self.assertNotContains(
            response,
            reverse('aristotle_publishing:publish_item', args=[self.item._meta.model_name, self.item.id])
        )

    def test_published_item_does_not_display_under_active_development_alert(self):
        """Test that a published item does not display 'The item is under active development banner"""

        # Publish an item (but don't register it)
        pub.PublicationRecord.objects.create(
            content_type=ContentType.objects.get_for_model(_concept),
            object_id=self.item.pk,
            publisher=self.submitting_user,
            publication_date=timezone.now() - timedelta(days=2),
            permission=visibility_permission_choices.public
        )
        self.item.concept.recache_states()
        # Check that it is publicly accessible
        self.logout()
        response = self.client.get(self.item.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        # Assert that the banner does not appear
        self.assertNotContains(response, 'This item is under active development')
