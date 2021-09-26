import requests
import logging
import os
from urllib.parse import urljoin

from django.dispatch import receiver

from allauth.account.signals import user_signed_up, user_logged_in

from webapp.models import Profile
from project.settings import CRF_API_URL_BASE, CRF_API_HEADERS


log = logging.getLogger('django')


@receiver(user_signed_up)
def on_user_signed_up(sender, **kwargs):
    """Create CRF lead for newly signed up user."""
    try:
        user = kwargs['user']
        response = requests.post(
            url=urljoin(CRF_API_URL_BASE, 'patient.json'),
            headers=CRF_API_HEADERS,
            data={'email': user.email})
        response.raise_for_status()
        crf_patient = response.json()
        profile = Profile(user=user, crf_patient_pk=crf_patient['pk'])
        profile.save()
    except Exception as err:
        log.error(str(err), exc_info=err)


@receiver(user_logged_in)
def on_user_logged_in(sender, **kwargs):
    "FOR TESTING"
    try:
        user = kwargs['user']
        crf_patient_pk = Profile.objects.get(user=user).crf_patient_pk
        response = requests.get(
            url=urljoin(
                CRF_API_URL_BASE,
                'patient/{}.json'.format(crf_patient_pk)),
            headers=CRF_API_HEADERS)
        response.raise_for_status()
        data = response.json()
        pass
    except Exception as err:
        log.error(str(err), exc_info=err)