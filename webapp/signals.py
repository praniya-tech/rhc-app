from django.dispatch import receiver
import requests
import logging

from allauth.account.signals import user_signed_up, user_logged_in


log = logging.getLogger('__name__')


@receiver(user_logged_in)
def on_user_signed_up(sender, **kwargs):
    """Create CRF lead for newly signed up user."""
    # try:
    user = kwargs['user']
    response = requests.post(
        url='http://localhost:8000/rhcapi/patient',
        data={'email': user.email})
    response.raise_for_status()
    # except Exception as err:
    #     log.error(str(err), exc_info=err)
