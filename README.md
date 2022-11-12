# Invictus Bier Systeem (backend)

```
python -m pipenv shell
```

daarna

```
python manage.py runserver
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