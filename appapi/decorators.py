import requests
from functools import wraps

from django.http import HttpResponseRedirect
from django.contrib import messages

from rest_framework.response import Response

from project.settings import DJANGO_LOGGER


def wrap_api(template_name=None, log_enabled=True):
    """
    Handle API exceptions. Returns response with status if available in case of
    exception.

    Specify `template_name` passing to wrapped API for 'html' response format.
    It is also passed to `Response` in case of exception to suppress error in
    case of 'html' response format.
    Logs exception to "django" logger if `log_enabled` is `True` (default).
    """
    def _decorator(api_func, **kwargs):
        @wraps(api_func)
        def _wrap_api(self, request, **kwargs):
            try:
                kwargs['template_name'] = template_name
                return api_func(self, request, **kwargs)
            except Exception as err:
                if log_enabled:
                    DJANGO_LOGGER.error(str(err), exc_info=err)
                if hasattr(err, 'response') and err.response:
                    return Response(
                        exception=True, status=err.response.status,
                        template_name=template_name)
                return Response(status=500, template_name=template_name)
        return _wrap_api
    return _decorator


def wrap_api_redirect(redirect_to=None, error_message=None, log_enabled=True):
    """
    Handle API exceptions. Redirects to specified `redirect_to` in case of
    exception with specified `error_message` set in Django `messages`.

    Specify `redirect_to` URL to pass to wrapped API and to redirect to in case
    of exception.
    Logs exception to "django" logger if `log_enabled` is `True` (default).
    """
    def _decorator(api_func, **kwargs):
        @wraps(api_func)
        def _wrap_api(self, request, **kwargs):
            try:
                kwargs['redirect_to'] = redirect_to
                return api_func(self, request, **kwargs)
            except Exception as err:
                if log_enabled:
                    DJANGO_LOGGER.error(str(err), exc_info=err)
                if error_message:
                    messages.error(request, error_message)
                if hasattr(err, 'response') and err.response:
                    return HttpResponseRedirect(redirect_to=redirect_to)
                return HttpResponseRedirect(redirect_to=redirect_to)
        return _wrap_api
    return _decorator
