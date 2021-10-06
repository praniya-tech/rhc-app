from django.urls import path
from django.views.generic import TemplateView
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from django.contrib.auth.decorators import login_required

from webapp.views import (
    HomeView, SvasthyaQuestionnaireView, HealthAssessmentView)


urlpatterns = [
    path(
        'favicon.ico',
        RedirectView.as_view(url=staticfiles_storage.url('webapp/favicon.png'))
    ),
    path('', HomeView.as_view(template_name='webapp/index.html')),
    path(
        'about-rasayu',
        TemplateView.as_view(template_name='webapp/about_rasayu.html'),
        name='rhcapp_about_rasayu'),
    path(
        'about',
        TemplateView.as_view(template_name='webapp/about.html'),
        name='rhcapp_about'),
    path(
        'tos',
        TemplateView.as_view(template_name='webapp/tos.html'),
        name='rhcapp_tos'),
    path(
        'health-assessment',
        login_required(
            HealthAssessmentView.as_view(
                template_name='webapp/health_assessment.html')),
        name='rhcapp_health_assessment'),
    path(
        'svasthya-questionnaire',
        login_required(
            SvasthyaQuestionnaireView.as_view(
                template_name='webapp/svasthya_questionnaire.html')),
        name='rhcapp_svasthya_questionnaire'),
    path(
        'svasthya-questionnaire/<int:id>/',
        login_required(
            SvasthyaQuestionnaireView.as_view(
                template_name='webapp/svasthya_questionnaire.html')),
        name='rhcapp_svasthya_questionnaire'),
    path(
        'prakriti-assessment',
        login_required(
            TemplateView.as_view(
                template_name='webapp/prakriti_assessment.html')),
        name='rhcapp_prakriti_assessment'),
]
