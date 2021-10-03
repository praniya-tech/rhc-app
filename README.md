# Suprajā Abhiyān app
Live a long, happy and fulfilling life with easy to follow presonalised and
preventive healthcare recommendations based on Āyurveda.

A public welfare initiative by [Rasāyu](https://app.rasayu.com/about-rasayu).


# Development setup

## Set `TokenAuthentication` for CRF RHC app API
RHC app API uses
[`TokenAuthentication`](https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication)
for accessing CRF RHC app API. In the CRF project, create a token for a CRF
superuser or a user having the required permissions using Django management
command
[`drf_create_token`](https://www.django-rest-framework.org/api-guide/authentication/#using-django-managepy-command).
Set the generated token in `RHCAPP_AUTH_TOKEN` environment variable.

## Package changes

### `django-adminlte3`

#### `adminlte3/templates/adminlte/lib/_main_header.html`

`webapp` overrides this template. Make following changes in this template:

1. Hide "messages" and "notifications" icons in the navbar for now.
   1. Add `{% block messages %}` to `<!-- Messages Dropdown Menu -->`.
   1. Add `{% block notifications %}` to `<!-- Notifications Dropdown Menu -->`.

2. Add `{% block nav_bar_left %}` to `<!-- Left navbar links -->`.
