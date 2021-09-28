import requests
from urllib.parse import urljoin
import json

from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response

from appapi.serializers import (
    SvasthyaQuestionnaireSerializer, SvasthyaQuestionTypeSerializer)
from project.settings import CRF_API_URL_BASE, CRF_API_HEADERS, DJANGO_LOGGER


class SvasthyaQuestionTypeViewSet(viewsets.ViewSet):
    def list(self, request, format=None):
        response = requests.get(
            url=urljoin(CRF_API_URL_BASE, 'svasthyaquestiontype.json'),
            headers=CRF_API_HEADERS)
        response.raise_for_status()
        questiontypes_json = response.json()
        questiontypes = SvasthyaQuestionTypeSerializer(
            questiontypes_json['results'], many=True).data
        return Response(questiontypes)


class SvasthyaQuestionnaireViewSet(viewsets.ViewSet):
    # https://stackoverflow.com/questions/18925358/how-do-you-access-data-in-the-template-when-using-drf-modelviewset-and-templateh
    renderer_classes = (JSONRenderer, TemplateHTMLRenderer)

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

    def create(self, request, format=None):
        questions = []
        question_orders = [
            v for k, v in request.data.items() if k.startswith('q')]
        responses = [
            v for k, v in request.data.items() if k.startswith('r')]
        for qo, r in zip(question_orders, responses):
            questions.append({
                'question': {
                    'order': int(qo)
                },
                'response': int(r)
            })
        questionnaire = {
            'patient_id': request.user.profile.crf_patient_pk,
            'questions': questions,
        }
        response = requests.post(
            url=urljoin(CRF_API_URL_BASE, 'svasthyaquestionnaire.json'),
            headers=CRF_API_HEADERS,
            json=questionnaire)
        response.raise_for_status()
        # https://stackoverflow.com/questions/18925358/how-do-you-access-data-in-the-template-when-using-drf-modelviewset-and-templateh
        if request.accepted_renderer.format == 'html':
            return Response(
                {'added_questionnaire': response.data},
                template_name='webapp/health_assessment.html')
        else:
            return response.data
