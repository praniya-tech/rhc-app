# rhc-app
Rasāyu healthcare app API and web app.


# Development setup

## Package changes

### `django-adminlte3`

- Hide "messages" and "notifications" icons in the navbar for now. Update the
  overridden template `adminlte3/templates/adminlte/lib/_main_header.html`:
  - Add `{% block messages %}` to `<!-- Messages Dropdown Menu -->`.
  - Add `{% block notifications %}` to `<!-- Notifications Dropdown Menu -->`.