import requests
from urllib.parse import urljoin
import json
from datetime import datetime, timedelta

from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.template import loader
from django.utils.translation import gettext as _
from django.utils.html import format_html

from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.decorators import action

from appapi.serializers import (
    SvasthyaQuestionnaireSerializer, SvasthyaQuestionTypeSerializer,
    PrakritiPropertyTypeSerializer)
from appapi.decorators import wrap_api, wrap_api_redirect

from project.settings import CRF_API_URL_BASE, CRF_API_HEADERS


class SvasthyaQuestionTypeViewSet(viewsets.ViewSet):
    renderer_classes = (JSONRenderer, TemplateHTMLRenderer)

    @wrap_api(template_name='appapi/components/svasthya_questionnaire.html')
    def list(self, request, format=None, template_name=None):
        response = requests.get(
            url=urljoin(CRF_API_URL_BASE, 'svasthyaquestiontype.json'),
            headers=CRF_API_HEADERS)
        response.raise_for_status()
        question_types_json = response.json()
        question_types = SvasthyaQuestionTypeSerializer(
            question_types_json, many=True).data
        context = {
            'question_types': question_types,
        }
        if request.accepted_renderer.format == 'html':
            template = loader.get_template(template_name)
            return HttpResponse(template.render(context, request))
        else:
            return Response(context)


class SvasthyaQuestionnaireViewSet(viewsets.ViewSet):
    # https://stackoverflow.com/questions/18925358/how-do-you-access-data-in-the-template-when-using-drf-modelviewset-and-templateh
    renderer_classes = (JSONRenderer, TemplateHTMLRenderer)

    @wrap_api(
        template_name='appapi/components/svasthya_questionnaires_card.html')
    def list(self, request, format=None, template_name=None):
        response = requests.get(
            url=urljoin(CRF_API_URL_BASE, 'svasthyaquestionnaire.json'),
            headers=CRF_API_HEADERS,
            data={'patient_id': request.user.profile.crf_patient_pk})
        response.raise_for_status()
        questionnaires_json = response.json()
        # questionnaires = SvasthyaQuestionnaireSerializer(
        #     questionnaires_json['results'], many=True).data
        questionnaires = questionnaires_json['results']
        context = {
            'svasthya_questionnaires': questionnaires,
            'next_assessment_date': None,
        }
        if len(questionnaires) > 0:
            # questionnaires are sorted descending by date, so first
            # questionnaire is the latest.
            last_assessment_date = (
                questionnaires_json['results'][0]['date']
                if len(questionnaires_json['results']) > 0
                else None
            )
            if last_assessment_date:
                next_assessment_date = (
                    datetime.strptime(last_assessment_date, '%d/%m/%Y')
                    + timedelta(days=30))
                context["next_assessment_date"] = next_assessment_date
        if request.accepted_renderer.format == 'html':
            if len(questionnaires) > 0:
                template = loader.get_template(template_name)
                return HttpResponse(template.render(context, request))
            else:
                return HttpResponse('')
        else:
            return context

    @wrap_api_redirect(
        redirect_to=reverse_lazy('webapp:wellness_assessment'),
        error_message=format_html(_(
            'Sorry, failed to save the questionnaire. Please try again later.'
            ' Please <a href=mailto:app.support@rasayu.com>contact us</a> at'
            ' app[dot]support[at]rasayu[dot]com if the problem persists.'
        )))
    def create(self, request, format=None, redirect_to=None):
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
            #added_questionnaire = response.json()
            return HttpResponseRedirect(redirect_to=redirect_to)
        else:
            return response.data

    @wrap_api(template_name='appapi/components/svasthya_questionnaire.html')
    def retrieve(self, request, pk=None, format=None, template_name=None):
        context = {}
        response = requests.get(
            url=urljoin(
                CRF_API_URL_BASE,
                'svasthyaquestionnaire/{}.json'.format(pk)),
            headers=CRF_API_HEADERS,
            json={
                'patient_id': request.user.profile.crf_patient_pk
            })
        response.raise_for_status()
        context['questionnaire'] = response.json()
        if request.accepted_renderer.format == 'html':
            template = loader.get_template(template_name=template_name)
            return HttpResponse(template.render(context, request))
        else:
            return context

    @action(detail=False)
    @wrap_api(template_name='appapi/components/last_wellness_assessment.html')
    def last_assessment_date(self, request, format=None, template_name=None):
        next_assessment_date = None
        if self.request.user.is_authenticated:
            patient_id = request.user.profile.crf_patient_pk
            response = requests.get(
                url=urljoin(
                    CRF_API_URL_BASE,
                    'svasthyaquestionnaire/last_assessment_date/'),
                headers=CRF_API_HEADERS,
                json={'patient_id': patient_id})
            response.raise_for_status()
            last_assessment_date = response.json()['last_assessment_date']
            if last_assessment_date:
                next_assessment_date = (
                    datetime.strptime(last_assessment_date, '%d/%m/%Y')
                    + timedelta(days=30))
        context = {
            "next_assessment_date": next_assessment_date,
        }
        if request.accepted_renderer.format == 'html':
            template = loader.get_template(template_name)
            return HttpResponse(template.render(context, request))
        else:
            return context


class PrakritiPropertyTypeViewSet(viewsets.ViewSet):
    renderer_classes = (JSONRenderer, TemplateHTMLRenderer)

    @wrap_api(
        template_name='appapi/components/prakriti_questionnaire_form.html')
    def list(self, request, format=None, template_name=None):
        response = requests.get(
            url=urljoin(CRF_API_URL_BASE, 'prakritipropertytype.json'),
            headers=CRF_API_HEADERS)
        response.raise_for_status()
        propertytypes_json = response.json()
        propertytypes = PrakritiPropertyTypeSerializer(
            propertytypes_json, many=True).data
        if request.accepted_renderer.format == 'html':
            context = {
                'property_types': propertytypes,
            }
            template = loader.get_template(template_name)
            return HttpResponse(template.render(context, request))
        else:
            return Response(propertytypes)
