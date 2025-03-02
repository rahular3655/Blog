from django.utils.translation import gettext_lazy as _
from drf_spectacular.extensions import OpenApiAuthenticationExtension
from drf_spectacular.openapi import AutoSchema
from drf_spectacular.utils import OpenApiParameter

"""
Global settings for api
"""


class BlogAutoSchema(AutoSchema):
    global_params = [
        OpenApiParameter(
            name="Accept-Language",
            type=str,
            location=OpenApiParameter.HEADER,
            description="chosen language",
            allow_blank=False,
            # required=True
        )
    ]

    def get_override_parameters(self):
        params = super().get_override_parameters()
        return params + self.global_params


class KnoxTokenScheme(OpenApiAuthenticationExtension):
    target_class = 'knox.auth.TokenAuthentication'
    name = 'knoxTokenAuth'

    def get_security_definition(self, auto_schema):
        return {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': _(
                'Token-based authentication with required prefix "%s"'
            ) % "Token"
        }
