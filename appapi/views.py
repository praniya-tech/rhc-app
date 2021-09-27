import requests
from urllib.parse import urljoin

from rest_framework import viewsets
from rest_framework.response import Response

from appapi.serializers import SvasthyaQuestionnaireSerializer
from project.settings import CRF_API_URL_BASE, CRF_API_HEADERS, DJANGO_LOGGER


# class SvasthyaQuestionViewSet

class SvasthyaQuestionnaireViewSet(viewsets.ViewSet):
    def list(self, request, format=None):
        response = requests.get(
            url=urljoin(CRF_API_URL_BASE, 'svasthyaquestionnaire.json'),
            headers=CRF_API_HEADERS,
            data={'patient_id': request.user.profile.crf_patient_pk})
        response.raise_for_status()
        questionnaires_json = response.json()
        questionnaires = SvasthyaQuestionnaireSerializer(
            questionnaires_json['results'], many=True).data
        return Response(questionnaires)
