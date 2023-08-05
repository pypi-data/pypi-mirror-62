from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
import aristotle_mdr.models as models
import aristotle_mdr.perms as perms
import aristotle_mdr.tests.utils as utils


class WorkgroupMembership(TestCase):
    """ Test permissions around workgroup management"""

    def setUp(self):
        self.steward_org_1 = models.StewardOrganisation.objects.create(
            name='Org 1',
            description="1",
        )

    def test_userInWorkgroup(self):
        wg = models.Workgroup.objects.create(name="Test WG 1", stewardship_organisation=self.steward_org_1)
        user = get_user_model().objects.create_user('editor1@example.com', 'editor1')
        wg.giveRoleToUser('viewer', user)
        self.assertTrue(perms.user_in_workgroup(user, wg))

    def test_RemoveUserFromWorkgroup(self):
        # Does removing a user from a workgroup remove their permissions? It should!
        wg = models.Workgroup.objects.create(name="Test WG 1", stewardship_organisation=self.steward_org_1)
        user = get_user_model().objects.create_user('editor1@example.com', 'editor1')
        wg.giveRoleToUser('manager', user)
        # Caching issue, refresh from DB with correct permissions
        user = get_user_model().objects.get(pk=user.pk)
        self.assertTrue(perms.user_in_workgroup(user, wg))
        self.assertTrue(perms.user_is_workgroup_manager(user, wg))
        wg.removeUser(user)
        # Caching issue, refresh from DB with correct permissions
        user = get_user_model().objects.get(pk=user.pk)
        self.assertFalse(perms.user_is_workgroup_manager(user, wg))

    def test_managersCanEditWorkgroups(self):
        wg = models.Workgroup.objects.create(name="Test WG 1", stewardship_organisation=self.steward_org_1)
        user1 = get_user_model().objects.create_user('manager@example.com', 'manager')
        user2 = get_user_model().objects.create_user('viewer@example.com', 'viewer')
        wg.giveRoleToUser('manager', user1)
        wg.giveRoleToUser('viewer', user2)
        wg.save()
        wg = models.Workgroup.objects.get(pk=wg.id)

        self.assertTrue(perms.user_in_workgroup(user1, wg))
        self.assertTrue(perms.user_in_workgroup(user2, wg))
        self.assertTrue(perms.user_can_view(user2, wg))
        self.assertTrue(perms.user_can_view(user1, wg))

        self.assertTrue(perms.user_can_edit(user1, wg))
        self.assertFalse(perms.user_can_edit(user2, wg))
        wg.removeUser(user1)
        wg.removeUser(user2)
        # Caching issue, refresh from DB with correct permissions
        user1 = get_user_model().objects.get(pk=user1.pk)
        user2 = get_user_model().objects.get(pk=user2.pk)
        self.assertFalse(perms.user_can_edit(user1, wg))
        self.assertFalse(perms.user_can_edit(user2, wg))

    def test_editable_workgroups_are_unique(self):
        # Tests against bug #333
        # https://github.com/aristotle-mdr/aristotle-metadata-registry/issues/333
        wg1 = models.Workgroup.objects.create(name="Test WG 1", stewardship_organisation=self.steward_org_1)
        wg2 = models.Workgroup.objects.create(name="Test WG 2", stewardship_organisation=self.steward_org_1)
        wg3 = models.Workgroup.objects.create(name="Test WG 3", stewardship_organisation=self.steward_org_1)
        editor = get_user_model().objects.create_user('editor@example.com', 'editor')
        wg1.giveRoleToUser('steward', editor)
        wg2.giveRoleToUser('steward', editor)
        wg3.giveRoleToUser('viewer', editor)
        wg1.save()
        wg2.save()
        wg3.save()

        editor = get_user_model().objects.get(pk=editor.pk)

        editable = editor.profile.editable_workgroups
        self.assertTrue(editable.count() == 2)
        self.assertTrue(wg1 in editable.all())
        self.assertTrue(wg2 in editable.all())
        self.assertTrue(wg3 not in editable.all())


class WorkgroupAnonTests(utils.LoggedInViewPages, TestCase):
    def test_anon_cannot_add(self):
        self.logout()
        response = self.client.get(reverse('aristotle:addWorkgroupMembers', args=[self.wg1.id]))
        self.assertRedirects(response,
                             reverse("friendly_login", ) + "?next=" +
                             reverse('aristotle:addWorkgroupMembers', args=[self.wg1.id])
                             )

        response = self.client.get(
            reverse('aristotle:registrationauthority_member_remove', args=[self.wg1.id, self.newuser.pk]))
        self.assertRedirects(response,
                             reverse("friendly_login", ) + "?next=" +
                             reverse('aristotle:registrationauthority_member_remove',
                                     args=[self.wg1.id, self.newuser.pk])
                             )

        response = self.client.post(
            reverse('aristotle:addWorkgroupMembers', args=[self.wg1.id]),
            {
                'roles': ['Viewer'],
                'users': [self.newuser.pk]
            }
        )
        self.assertRedirects(
            response,
            reverse("friendly_login", ) + "?next=" +
            reverse('aristotle:addWorkgroupMembers', args=[self.wg1.id])
        )
        self.assertListEqual(list(self.newuser.profile.workgroups.all()), [])


class WorkgroupCreationTests(utils.LoggedInViewPages, TestCase):
    def test_anon_cannot_create(self):
        self.logout()
        response = self.client.get(reverse('aristotle:workgroup_create'))
        self.assertRedirects(response,
                             reverse("friendly_login", ) + "?next=" +
                             reverse('aristotle:workgroup_create')
                             )

    def test_viewer_cannot_create(self):
        self.login_viewer()

        response = self.client.get(reverse('aristotle:workgroup_create'))
        self.assertEqual(response.status_code, 403)

        before_count = models.Workgroup.objects.count()
        response = self.client.post(
            reverse('aristotle:workgroup_create'),
            {
                'name': "My cool team",
                'definition': "This team rocks!"
            }
        )
        self.assertEqual(response.status_code, 403)
        after_count = models.Workgroup.objects.count()
        self.assertEqual(after_count, before_count)

    def test_manager_cannot_create(self):
        self.login_manager()

        response = self.client.get(reverse('aristotle:workgroup_create'))
        self.assertEqual(response.status_code, 403)

        before_count = models.Workgroup.objects.count()
        response = self.client.post(
            reverse('aristotle:workgroup_create'),
            {
                'name': "My cool team",
                'definition': "This team rocks!"
            }
        )
        self.assertEqual(response.status_code, 403)
        after_count = models.Workgroup.objects.count()
        self.assertEqual(after_count, before_count)

    def test_registry_owner_can_create(self):
        self.login_superuser()

        response = self.client.get(reverse('aristotle:workgroup_create'))
        self.assertEqual(response.status_code, 200)

        before_count = models.Workgroup.objects.count()
        response = self.client.post(
            reverse('aristotle:workgroup_create'),
            {
                'name': "My cool team",
                'definition': "This team rocks!",
                'stewardship_organisation': self.steward_org_1.uuid,
            },
            follow=True
        )

        self.assertTrue(response.redirect_chain[0][1] == 302)

        self.assertEqual(response.status_code, 200)
        after_count = models.Workgroup.objects.count()
        self.assertEqual(after_count, before_count + 1)

        # new_wg = models.Workgroup.objects.order_by('-created').first()
        new_wg = response.context['item']

        self.assertEqual(new_wg.name, "My cool team")
        self.assertEqual(new_wg.definition, "This team rocks!")


class WorkgroupUpdateTests(utils.LoggedInViewPages, TestCase):
    def test_anon_cannot_update(self):
        self.logout()
        response = self.client.get(reverse('aristotle:workgroup_create'))
        self.assertRedirects(response,
                             reverse("friendly_login", ) + "?next=" +
                             reverse('aristotle:workgroup_create')
                             )

    def test_viewer_cannot_update(self):
        self.login_viewer()

        my_wg = models.Workgroup.objects.create(name="My new Workgroup", definition="",
                                                stewardship_organisation=self.steward_org_1)

        response = self.client.get(reverse('aristotle:workgroup_edit', args=[my_wg.pk]))
        self.assertEqual(response.status_code, 403)

        data = {
            'name': "My cool registrar",
            'definition': "This Workgroup rocks!"
        }

        response = self.client.post(
            reverse('aristotle:workgroup_edit', args=[my_wg.pk]),
            data
        )
        self.assertEqual(response.status_code, 403)
        my_wg = models.Workgroup.objects.get(pk=my_wg.pk)

        self.assertNotEqual(my_wg.name, "My cool registrar")
        self.assertNotEqual(my_wg.definition, "This Workgroup rocks!")

    def test_registry_owner_can_edit(self):
        self.login_superuser()

        my_wg = models.Workgroup.objects.create(name="My new Workgroup", definition="",
                                                stewardship_organisation=self.steward_org_1)

        response = self.client.get(reverse('aristotle:workgroup_edit', args=[my_wg.pk]))
        self.assertEqual(response.status_code, 200)

        data = response.context['form'].initial
        data.update({
            'name': "My cool registrar",
            'definition': "This Workgroup rocks!"
        })
        response = self.client.post(
            reverse('aristotle:workgroup_edit', args=[my_wg.pk]),
            data
        )
        self.assertEqual(response.status_code, 302)
        my_wg = models.Workgroup.objects.get(pk=my_wg.pk)

        self.assertEqual(my_wg.name, "My cool registrar")
        self.assertEqual(my_wg.definition, "This Workgroup rocks!")

    def test_manager_can_edit(self):
        self.login_manager()

        my_wg = models.Workgroup.objects.create(name="My new Workgroup", definition="",
                                                stewardship_organisation=self.steward_org_1)

        response = self.client.get(reverse('aristotle:workgroup_edit', args=[my_wg.pk]))
        self.assertEqual(response.status_code, 403)

        my_wg.giveRoleToUser('manager', self.manager)
        my_wg = models.Workgroup.objects.get(pk=my_wg.pk)
        self.assertTrue(my_wg.has_role('manager', self.manager))

        response = self.client.get(reverse('aristotle:workgroup_edit', args=[my_wg.pk]))
        self.assertEqual(response.status_code, 200)

        data = response.context['form'].initial
        data.update({
            'name': "My cool registrar",
            'definition': "This Workgroup rocks!",
        })

        response = self.client.post(
            reverse('aristotle:workgroup_edit', args=[my_wg.pk]),
            data
        )
        self.assertEqual(response.status_code, 302)
        my_wg = models.Workgroup.objects.get(pk=my_wg.pk)

        self.assertEqual(my_wg.name, "My cool registrar")
        self.assertEqual(my_wg.definition, "This Workgroup rocks!")


class WorkgroupListTests(utils.LoggedInViewPages, TestCase):
    def test_anon_cannot_list(self):
        self.logout()
        response = self.client.get(reverse('aristotle:workgroup_list'))
        self.assertRedirects(response,
                             reverse("friendly_login", ) + "?next=" +
                             reverse('aristotle:workgroup_list')
                             )

    def test_viewer_cannot_list(self):
        self.login_viewer()

        response = self.client.get(reverse('aristotle:workgroup_list'))
        self.assertEqual(response.status_code, 403)

    def test_manager_cannot_list(self):
        self.login_manager()

        response = self.client.get(reverse('aristotle:workgroup_list'))
        self.assertEqual(response.status_code, 403)

    def test_registry_owner_can_list(self):
        self.login_superuser()

        response = self.client.get(reverse('aristotle:workgroup_list'))
        self.assertEqual(response.status_code, 200)


class WorkgroupMemberTests(utils.LoggedInViewPages, TestCase):
    def test_all_workgroup_items_are_displayed_on_workgroup_item_page(self):
        """Test all workgroup items are displayed on workgroup item page"""
        self.login_superuser()  # Not checking viewing permissions in this test
        for i in range(0, 7):
            models.ObjectClass.objects.create(name=f"Snow White and the {i}th Dwarf",
                                              workgroup=self.wg1)
        response = self.client.get(reverse('aristotle:workgroupItems', args=[self.wg1.id]))
        self.assertResponseStatusCodeEqual(response=response, code=200)
        self.assertEqual(len(response.context['object_list']), 7)

        for i in range(0, 7):
            self.assertContainsHtml(response, f'Snow White and the {i}th Dwarf')

    def test_user_can_leave_workgroup(self):
        self.login_viewer()
        response = self.client.get(self.wg1.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        self.assertTrue(perms.user_in_workgroup(self.viewer, self.wg1))

        response = self.client.get(reverse('aristotle:workgroup_leave', args=[self.wg1.id]))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('aristotle:workgroup_leave', args=[self.wg1.id]))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(self.wg1.get_absolute_url())
        self.assertEqual(response.status_code, 403)

    def test_viewer_cannot_add_change_or_remove_users(self):
        self.login_viewer()
        response = self.client.get(reverse('aristotle:addWorkgroupMembers', args=[self.wg1.id]))
        self.assertEqual(response.status_code, 403)
        response = self.client.get(
            reverse('aristotle:workgroup_member_change_role', args=[self.wg1.id, self.newuser.pk]))
        self.assertEqual(response.status_code, 403)
        response = self.client.get(reverse('aristotle:workgroup_member_remove', args=[self.wg1.id, self.newuser.pk]))
        self.assertEqual(response.status_code, 403)

    def test_viewer_cannot_see_add_user_button(self):
        """ The viewer should not be able to see the Add User button in the workgroup member list, as
            they are not permitted to add users"""
        self.login_viewer()

        response = self.client.get(reverse('aristotle:workgroupMembers', args=[self.wg1.id]))

        self.assertNotContainsHtml(response, 'Add a user')

    def test_manager_can_see_add_user_button(self):
        """ Managers should be able to see the Add User button in the workgroup member list"""
        self.login_manager()

        response = self.client.get(reverse('aristotle:workgroupMembers', args=[self.wg1.id]))

        self.assertContainsHtml(response, 'Add a user')

    def test_manager_can_add_or_change_users(self):
        self.login_manager()
        self.assertTrue(self.newuser in list(get_user_model().objects.all()))

        response = self.client.get(reverse('aristotle:addWorkgroupMembers', args=[self.wg2.id]))
        self.assertEqual(response.status_code, 403)
        response = self.client.get(reverse('aristotle:addWorkgroupMembers', args=[self.wg1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.newuser.id in [u[0] for u in response.context['form'].fields['user'].choices])

        self.assertListEqual(list(self.newuser.profile.workgroups.all()), [])
        response = self.client.post(
            reverse('aristotle:addWorkgroupMembers', args=[self.wg2.id]),
            {
                'role': 'viewer',
                'user': self.newuser.pk
            }
        )
        self.assertEqual(response.status_code, 403)
        self.assertListEqual(list(self.newuser.profile.workgroups.all()), [])

        response = self.client.post(
            reverse('aristotle:addWorkgroupMembers', args=[self.wg1.id]),
            {
                'role': 'viewer',
                'user': self.newuser.pk
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.newuser in self.wg1.member_list.all())
        self.assertListEqual(list(self.newuser.profile.workgroups.all()), [self.wg1])

        response = self.client.get(
            reverse('aristotle:workgroup_member_change_role', args=[self.wg1.id, self.newuser.pk]))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('aristotle:workgroup_member_change_role', args=[self.wg1.id, self.newuser.pk]),
            {'role': 'manager'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.wg1.has_role('manager', self.newuser))
        self.assertFalse(self.wg1.has_role('viewer', self.newuser))

    def test_manager_can_remove_users(self):
        self.login_manager()
        self.assertTrue(self.newuser in list(get_user_model().objects.all()))

        response = self.client.post(
            reverse('aristotle:addWorkgroupMembers', args=[self.wg1.id]),
            {
                'role': 'manager',
                'user': self.newuser.pk
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.newuser in self.wg1.member_list.all())
        self.assertFalse(self.wg1.has_role('viewer', self.newuser))
        self.assertTrue(self.wg1.has_role('manager', self.newuser))
        self.assertListEqual(list(self.newuser.profile.workgroups.all()), [self.wg1])

        response = self.client.post(
            reverse('aristotle:workgroup_member_remove', args=[self.wg1.id, self.newuser.pk]),
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.wg1.has_role('viewer', self.newuser))
        self.assertFalse(self.wg1.has_role('manager', self.newuser))

        response = self.client.get(
            reverse('aristotle:workgroup_member_remove', args=[self.wg1.id, self.newuser.pk]),
        )

    def test_workgroup_members_can_view_pages(self):
        self.logout()
        # Anonymous user can't see workgroup pages
        n = reverse('friendly_login') + "?next="
        response = self.client.get(reverse('aristotle:workgroup', args=[self.wg1.id]))
        self.assertRedirects(response, n + reverse('aristotle:workgroup', args=[self.wg1.id]), 302, 200)
        response = self.client.get(reverse('aristotle:workgroupMembers', args=[self.wg1.id]))
        self.assertRedirects(response, n + reverse('aristotle:workgroupMembers', args=[self.wg1.id]), 302, 200)
        response = self.client.get(reverse('aristotle:workgroupItems', args=[self.wg1.id]))
        self.assertRedirects(response, n + reverse('aristotle:workgroupItems', args=[self.wg1.id]), 302, 200)

        # Logged in non-member can't see workgroup pages
        response = self.client.post(reverse('friendly_login'), {'username': 'nathan@example.com', 'password': 'noobie'})
        response = self.client.get(reverse('aristotle:workgroup', args=[self.wg1.id]))
        self.assertEqual(response.status_code, 403)

        response = self.client.get(self.wg1.get_absolute_url())
        self.assertEqual(response.status_code, 403)

        response = self.client.get(reverse('aristotle:workgroupMembers', args=[self.wg1.id]))
        self.assertEqual(response.status_code, 403)
        response = self.client.get(reverse('aristotle:workgroupItems', args=[self.wg1.id]))
        self.assertEqual(response.status_code, 403)

        self.login_viewer()
        response = self.client.get(reverse('aristotle:workgroup', args=[self.wg1.id]))
        self.assertRedirects(response, self.wg1.get_absolute_url())
        self.assertEqual(response.status_code, 302)
        response = self.client.get(self.wg1.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('aristotle:workgroupMembers', args=[self.wg1.id]))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('aristotle:workgroupItems', args=[self.wg1.id]))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(
            reverse('aristotle:workgroupItems', args=[self.wg1.id]) + "?page=100")  # deliberately overshoot
        self.assertEqual(response.status_code, 404)

        self.login_manager()

        response = self.client.get(reverse('aristotle:workgroup', args=[self.wg1.id]))
        self.assertEqual(response.status_code, 302)
        response = self.client.get(self.wg1.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('aristotle:workgroupMembers', args=[self.wg1.id]))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('aristotle:workgroupItems', args=[self.wg1.id]))

    def test_manager_can_archive(self):
        self.login_viewer()
        # Viewers cannot archive
        response = self.client.get(reverse('aristotle:archive_workgroup', args=[self.wg1.id]))
        self.assertEqual(response.status_code, 403)
        response = self.client.get(reverse('aristotle:archive_workgroup', args=[self.wg2.id]))
        self.assertEqual(response.status_code, 403)

        # Viewers shouldn't even have the button on the workgroup page
        response = self.client.get(self.wg1.get_absolute_url())
        self.assertNotContains(response, "archive_modal")

        self.login_manager()

        # Managers must have the archive button on the workgroup page
        response = self.client.get(self.wg1.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "archive_modal")

        response = self.client.get(reverse('aristotle:archive_workgroup', args=[self.wg2.id]))
        self.assertEqual(response.status_code, 403)
        response = self.client.get(reverse('aristotle:archive_workgroup', args=[self.wg1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.wg1.archived)
        self.assertTrue(self.wg1 in self.viewer.profile.myWorkgroups)

        response = self.client.post(reverse('aristotle:archive_workgroup', args=[self.wg1.id]), {})
        self.assertRedirects(response, self.wg1.get_absolute_url())

        self.wg1 = models.Workgroup.objects.get(pk=self.wg1.pk)  # refetch
        self.assertTrue(self.wg1.archived)
        self.assertTrue(self.wg1 not in self.viewer.profile.myWorkgroups)

        response = self.client.post(reverse('aristotle:archive_workgroup', args=[self.wg1.id]), {})
        self.assertRedirects(response, self.wg1.get_absolute_url())
        self.wg1 = models.Workgroup.objects.get(pk=self.wg1.pk)  # refetch
        self.assertFalse(self.wg1.archived)
        self.assertTrue(self.wg1 in self.viewer.profile.myWorkgroups)


class TestMyWorkgroups(utils.LoggedInViewPages, TestCase):
    def test_viewer_cannot_see_edit_button_for_workgroup(self):
        self.login_viewer()
        # Create a workgroup
        workgroup = models.Workgroup.objects.create(name="My new Workgroup",
                                                definition="",
                                                stewardship_organisation=self.steward_org_1)
        # Allow the viewer to view the workgroup
        workgroup.giveRoleToUser('viewer', self.viewer)

        response = self.client.get(reverse('aristotle:userWorkgroups'))

        # Assert that the 'Edit' button is not there
        self.assertNotContainsHtml(response, 'Edit')

    def test_superuser_can_see_edit_button_for_workgroup(self):
        self.login_superuser()

        workgroup = models.Workgroup.objects.create(name="My new Workgroup",
                                                    definition="",
                                                    stewardship_organisation=self.steward_org_1)
        # Allow the viewer to view the workgroup
        workgroup.giveRoleToUser('viewer', self.su)

        response = self.client.get(reverse('aristotle:userWorkgroups'))

        # Assert that the 'Edit' button is displayed
        self.assertContainsHtml(response, 'Edit')
