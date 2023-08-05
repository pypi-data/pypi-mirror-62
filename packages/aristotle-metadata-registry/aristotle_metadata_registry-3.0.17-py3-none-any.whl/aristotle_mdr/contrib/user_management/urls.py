from django.conf.urls import url, include
from aristotle_mdr.contrib.user_management import views, org_backends


urlpatterns = [
    # url(r'^accounts/signup', views.NewUserSignupView.as_view(), name="new_user_signup"),
    url(r'^account/registry/invitations/', include(org_backends.AristotleInvitationBackend().get_urls())),
    url(r'^account/signup/$', views.SignupView.as_view(), name='signup_register'),
    url(r'^account/signup/activate/(?P<user_id>[\d]+)-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.SignupActivateView.as_view(), name="signup_activate"),
    url(r'^account/signup/resend/', views.ResendActivationView.as_view(), name='signup_resend'),
    url(r'^account/registry/users/$', views.RegistryOwnerUserList.as_view(), name="registry_user_list"),
    url(r'^account/registry/users/(?P<user_pk>\d+)/?$', views.ViewAnotherUser.as_view(), name="view_another_user"),
    url(r'^account/registry/users/(?P<user_pk>\d+)/update$', views.UpdateAnotherUser.as_view(), name="update_another_user"),
    url(r'^account/registry/users/(?P<user_pk>\d+)/deactivate$', views.DeactivateRegistryUser.as_view(), name="deactivate_user"),
    url(r'^account/registry/users/(?P<user_pk>\d+)/reactivate$', views.ReactivateRegistryUser.as_view(), name="reactivate_user"),
    url(r'^account/registry/users/(?P<user_pk>\d+)/site-wide-permissions', views.UpdateAnotherUserSiteWidePerms.as_view(), name="update_another_user_site_perms"),
]
