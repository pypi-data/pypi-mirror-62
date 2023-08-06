# -*- coding: utf-8 -*-
# Copyright (c) 2016, 2017, 2018, 2019 Sqreen. All rights reserved.
# Please refer to our terms for more information:
#
#     https://www.sqreen.io/terms.html
#
""" Django specific WSGI HTTP Request / Response stuff
"""
from itertools import chain
from logging import getLogger

import pkg_resources

from ..utils import to_unicode_safe
from .base import BaseRequest, BaseResponse

LOGGER = getLogger(__name__)


def drf_preload_data():
    """Detect if request data should be preloaded for Django Rest Framework.

    See https://github.com/encode/django-rest-framework/issues/3951.
    """
    for package in pkg_resources.working_set:
        if package.project_name == "djangorestframework":
            drf_version_info = tuple(map(int, package.version.split(".")[:2]))
            return (3, 3) <= drf_version_info <= (3, 4)
    return False


class DjangoRequest(BaseRequest):

    DRF_PRELOAD_DATA = drf_preload_data()

    def __init__(self, request):
        super(DjangoRequest, self).__init__()
        self.request = request

        # Cache for params
        self._query_params = None
        self._query_params_values = None
        self._form_params = None

        if self.__class__.DEBUG_MODE is None:
            self.__class__.DEBUG_MODE = self.is_debug()

    @property
    def query_params(self):
        if self._query_params is None:
            # Convert django QueryDict to a normal dict with values as list
            self._query_params = dict(self.request.GET.lists())
        return self._query_params

    @property
    def query_params_values(self):
        """ Return only query values as a list
        """
        if self._query_params_values is None:
            self._query_params_values = list(
                chain.from_iterable(self.query_params.values())
            )
        return self._query_params_values

    @property
    def form_params(self):
        if self._form_params is None:
            try:
                if (
                    self.DRF_PRELOAD_DATA
                    and self.request.method == "POST"
                    and not getattr(self.request, "_read_started", False)
                ):
                    self.request.body

                self._form_params = dict(self.request.POST)
            except Exception:  # UnreadablePostError, RawPostDataException, RequestDataTooBig
                # TODO fallback to the future WSGI input stream preview
                self._form_params = {}
        return self._form_params

    @property
    def cookies_params(self):
        return self.request.COOKIES

    @property
    def remote_addr(self):
        return to_unicode_safe(self.get_raw_header("REMOTE_ADDR"))

    @property
    def hostname(self):
        return self.request.get_host()

    @property
    def method(self):
        return self.request.method

    @property
    def referer(self):
        return to_unicode_safe(self.get_raw_header("HTTP_REFERER"))

    @property
    def client_user_agent(self):
        return to_unicode_safe(self.get_raw_header("HTTP_USER_AGENT"))

    @property
    def route(self):
        """Request route."""
        # The resolver_match attribute is set only set once all request
        # middlewares have been called.
        resolver_match = getattr(self.request, "resolver_match", None)
        return getattr(resolver_match, "view_name", None)

    @property
    def path(self):
        return self.request.path

    @property
    def scheme(self):
        return getattr(self.request, "scheme", None)

    @property
    def server_port(self):
        return to_unicode_safe(self.get_raw_header("SERVER_PORT"))

    @property
    def remote_port(self):
        return to_unicode_safe(self.get_raw_header("REMOTE_PORT"))

    @property
    def raw_headers(self):
        return self.request.META

    @property
    def view_params(self):
        resolver_match = getattr(self.request, "resolver_match", None)
        if resolver_match:
            return resolver_match.kwargs

    @property
    def json_params(self):
        return {}

    @classmethod
    def is_debug(self):
        try:
            from django.conf import settings

            return getattr(settings, "DEBUG", False)
        except Exception:
            LOGGER.warning("Exception when checking debug mode", exc_info=1)
            return False


class DjangoResponse(BaseResponse):

    def __init__(self, response):
        self.response = response

    @property
    def status_code(self):
        return self.response.status_code

    @property
    def content_type(self):
        return self.response.get("Content-Type")

    @property
    def content_length(self):
        try:
            return int(self.response.get("Content-Length"))
        except (ValueError, TypeError):
            return None
