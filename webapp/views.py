import requests
from urllib.parse import urljoin
from datetime import datetime, timedelta

from django.shortcuts import render
from django.views.generic.base import View, TemplateView
from django.views.generic import CreateView
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
from django.urls import reverse

from project.settings import CRF_API_URL_BASE, CRF_API_HEADERS, DJANGO_LOGGER


class HomeView(TemplateView):
    template_name = 'webapp/index.html'

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            if self.request.user.is_authenticated:
                patient_id = self.request.user.profile.crf_patient_pk
                response = requests.get(
                    url=urljoin(
                        CRF_API_URL_BASE,
                        'svasthyaquestionnaire/last_assessment_date/'),
                    headers=CRF_API_HEADERS,
                    json={'patient_id': patient_id},)
                response.raise_for_status()
                last_assessment_date = response.json()['last_assessment_date']
                context["next_assessment_date"] = None
                if last_assessment_date:
                    next_assessment_date = (
                        datetime.strptime(last_assessment_date, '%d/%m/%Y')
                        + timedelta(days=30))
                    context["next_assessment_date"] = next_assessment_date
            return context
        except Exception as err:
            DJANGO_LOGGER.error(str(err), exc_info=err)


class SvasthyaQuestionnaireView(TemplateView):
    template_name = 'webapp/svasthya_questionnaire.html'

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            questionnaire_id = kwargs.get('id', None)
            if questionnaire_id:
                response = requests.get(
                    url=urljoin(
                        CRF_API_URL_BASE,
                        'svasthyaquestionnaire/{}.json'.format(
                            questionnaire_id)),
                    headers=CRF_API_HEADERS,
                    json={
                        'patient_id': self.request.user.profile.crf_patient_pk
                    })
                response.raise_for_status()
                context['questionnaire'] = response.json()
            else:
                response = requests.get(
                    url=urljoin(CRF_API_URL_BASE, 'svasthyaquestiontype.json'),
                    headers=CRF_API_HEADERS,
                    json={
                        'patient_id': self.request.user.profile.crf_patient_pk
                    })
                response.raise_for_status()
                question_types = response.json()
                context["question_types"] = question_types['results']
            return context
        except Exception as err:
            DJANGO_LOGGER.error(str(err), exc_info=err)


class HealthAssessmentView(TemplateView):
    template_name = 'webapp/health_assessment.html'

    def get_context_data(self, **kwargs):
        try:
            patient_id = self.request.user.profile.crf_patient_pk
            response = requests.get(
                url=urljoin(CRF_API_URL_BASE, 'svasthyaquestionnaire.json'),
                headers=CRF_API_HEADERS,
                json={'patient_id': patient_id},)
            response.raise_for_status()
            question_types = response.json()
            context = super().get_context_data(**kwargs)
            context["svasthya_questionnaires"] = question_types['results']
            last_assessment_date = (
                question_types['results'][-1]['date']
                if len(question_types['results']) > 0
                else None
            )
            context["next_assessment_date"] = None
            if last_assessment_date:
                next_assessment_date = (
                    datetime.strptime(last_assessment_date, '%d/%m/%Y')
                    + timedelta(days=30))
                context["next_assessment_date"] = next_assessment_date
            return context
        except Exception as err:
            DJANGO_LOGGER.error(str(err), exc_info=err)
