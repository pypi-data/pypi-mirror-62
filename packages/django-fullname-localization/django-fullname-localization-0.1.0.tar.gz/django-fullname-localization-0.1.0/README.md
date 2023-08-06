# django-fullname-localization

Add localization support for user's fullname.

## Install

```shell
pip install django-fullname-localization
```

## Settings

**pro/settings.py**

```python
INSTALLED_APPS = [
    ...
    'django_fullname_localization',
    ...
]
```

## Fullname template setting

FULL_NAME_TEMPLATE default to "{last_name}{first_name}", it's chinese default name format ^_^.
Supported paramters are:

- user
- last_name
- fisrt_name

If using default User model, you can user first_name and last_name parameter to write your own template.
If using customer model that has more name parts, you can using parameter {user.your_own_field}.

## Usage

**app/template/demo.html**

```html
{{request.user.get_full_name}}
```

**app/views.py**

```python

def page(request):
    ...
    fullname = request.user.get_fullname()
    ...
```


## Release

### v0.1.0 2020/02/29

- First release.

