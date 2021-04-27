"""
Oauth2 backend class to accept both multipart/form-data and application/json requests
https://github.com/jazzband/django-oauth-toolkit/issues/296#issuecomment-149233636
"""

import json

from oauth2_provider import oauth2_backends


class OAuthLibCore(oauth2_backends.OAuthLibCore):
    """Backend for Django Rest Framework"""

    def extract_body(self, request):
        """
        DRF object keeps data in request.DATA whether django request
        inside POST
        """
        if request.content_type == 'application/json':
            try:
                body = json.loads(request.body.decode("utf-8")).items()
            except AttributeError:
                body = ""
            except ValueError:
                body = ""

            return body

        return super().extract_body(request)
