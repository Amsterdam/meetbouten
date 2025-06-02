import amsterdam_django_oidc
from django.db import transaction
from django.http import HttpResponseRedirect
from django.urls import reverse


def oidc_login(request, **kwargs):
    oidc_authentication_init = reverse("oidc_authentication_init")
    redirect = f'{oidc_authentication_init}?next={request.GET.get("next", "")}'
    return HttpResponseRedirect(redirect)


class OIDCAuthenticationBackend(amsterdam_django_oidc.OIDCAuthenticationBackend):
    def create_user(self, claims):
        user = super(OIDCAuthenticationBackend, self).create_user(claims)
        return self.update_user(user, claims)

    def update_user(self, user, claims):
        user.first_name = claims.get("given_name", "")
        user.last_name = claims.get("family_name", "")
        user.save()
        self.update_groups(user, claims)
        return user

    def update_groups(self, user, claims):
        """
        We can use this method to update the groups of the user
        based on the roles passed by Azure AD. At the moment we receive none,
        and we assume any user that is able log in is an admin.
        """
        with transaction.atomic():
            user.groups.clear()
            user.is_staff = True
            user.is_superuser = True
            user.save()

    def authenticate(self, request, **kwargs):
        user = super().authenticate(request, **kwargs)
        # Ensure that the user does not come into an endless redirect loop
        # when they try to login in to the admin, but do not have the correct
        # role to edit sensors.
        if user and user.is_staff:
            return user
        return None
