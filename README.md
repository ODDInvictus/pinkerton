# Pinkerton (backend voor IBS)

Om ook maar iets te doen met de backend, moet je eerst een shell openen met

```
python -m pipenv shell
```

Hoe draai ik de server dan?

```
python manage.py runserver
```

## Voor het eerst opstarten

Voordat je ibs lokaal kan opstarten moet je eerst de database initializeren

```
python manage.py migrate
```

Daarna maak je een superuser aan

```
python manage.py createsuperuser
```

Met deze user kan je inloggen op http://127.0.0.1/admin

## Nieuwe dependency toevoegen
```
pipenv install {naam}
```

## Nieuwe app toevoegen

Voorbeeld: {app naam} app
```
mkdir ibs/{app naam}
```

daarna

```
python manage.py startapp {app naam} ibs/{app naam}
```

registreer daarna de app in ibs/settings.py

```py
INSTALLED_APPS = [
  ...
  'ibs.financial',
  'ibs.{app naam}'
]
```

Daarna moet je nog de naam aanpassen in ibs/{app naam}/apps.py

```py
class FinancialConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ibs.{app naam}'
```

Als laatst nog de urls aanmaken in urls.py

```py
urlpatterns = [
    path('api/admin/', admin.site.urls),

    # apps
    path('api/financial/', include('ibs.financial.urls')),
    path('api/{app naam}/', include('ibs.{app naam}.urls')),
]
```

en een urls.py aanmaken in de app zelf

```py
from django.urls import path

app_name = '{app naam}'

urlpatterns = []
```