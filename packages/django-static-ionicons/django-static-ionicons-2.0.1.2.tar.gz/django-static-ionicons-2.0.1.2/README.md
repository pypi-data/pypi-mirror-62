# django-static-ionicons


Django application contain ionicons static files


## Install


```shell
    pip install django-static-ionicons
```

## Settings

```python
INSTALLED_APPS = [
    ...
    "django_static_ionicons",
    ...
]
```

## Usage
-------------------

**app/templates/demo.html**

```python
{% load staticfiles %}

{% block style %}
    <link rel="stylesheet" type="text/css" href="{% static "ionicons/css/ionicons.css" %}">
{% endblock %}
```

## Releases

### v2.0.1.2 2020/02/26

- Add demo page.

### v2.0.1.1 2018/03/27

- Repackage.

### v2.0.1 2017/12/21

- First release.