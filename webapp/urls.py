from django.urls import path
from django.views.generic import TemplateView
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView


urlpatterns = [
    path(
        'favicon.ico',
        RedirectView.as_view(url=staticfiles_storage.url('webapp/favicon.png'))
    ),
    path('', TemplateView.as_view(template_name='webapp/index.html')),
    path(
        'about-rasayu',
        TemplateView.as_view(template_name='webapp/about_rasayu.html'),
        name='rhcapp_about_rasayu')
]
