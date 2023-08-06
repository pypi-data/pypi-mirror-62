# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_client.api.base import BaseApiHandler
from polyaxon_client.exceptions import PolyaxonClientException


class UserApi(BaseApiHandler):
    """
    Api handler to manage users.
    """
    ENDPOINT = "/users"
    ENDPOINT_SUPERUSERS = "/superusers"

    def activate_user(self, username):
        """Activate a user account."""
        request_url = self.build_url(self._get_http_url(), 'activate', username)

        try:
            return self.transport.post(request_url)
        except PolyaxonClientException as e:
            self.transport.handle_exception(e=e, log_message='Error while activating user.')
            return None

    def delete_user(self, username):
        """Delete a user account."""
        request_url = self.build_url(self._get_http_url(), 'delete', username)

        try:
            return self.transport.delete(request_url)
        except PolyaxonClientException as e:
            self.transport.handle_exception(e=e, log_message='Error while deleting user.')
            return None

    def grant_superuser(self, username):
        """Activate a user account."""
        request_url = self.build_url(self._get_http_url(self.ENDPOINT_SUPERUSERS),
                                     'grant',
                                     username)

        try:
            return self.transport.post(request_url)
        except PolyaxonClientException as e:
            self.transport.handle_exception(
                e=e, log_message='Error while grating superuser to user.')
            return None

    def revoke_superuser(self, username):
        """Activate a user account."""
        request_url = self.build_url(self._get_http_url(self.ENDPOINT_SUPERUSERS),
                                     'revoke',
                                     username)

        try:
            return self.transport.post(request_url)
        except PolyaxonClientException as e:
            self.transport.handle_exception(
                e=e, log_message='Error while revoking superuser to user.')
            return None
