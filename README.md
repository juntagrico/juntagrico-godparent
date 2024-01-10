# juntagrico-godparent

[![image](https://github.com/juntagrico/juntagrico-godparent/actions/workflows/juntagrico-ci.yml/badge.svg?branch=main&event=push)](https://github.com/juntagrico/juntagrico-godparent/actions/workflows/juntagrico-ci.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/f390c5529dcde5b83e85/maintainability)](https://codeclimate.com/github/juntagrico/juntagrico-godparent/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/f390c5529dcde5b83e85/test_coverage)](https://codeclimate.com/github/juntagrico/juntagrico-godparent/test_coverage)
[![image](https://img.shields.io/github/last-commit/juntagrico/juntagrico-godparent.svg)](https://github.com/juntagrico/juntagrico-godparent)
[![image](https://img.shields.io/github/commit-activity/y/juntagrico/juntagrico-godparent)](https://github.com/juntagrico/juntagrico-godparent)

Match godparents with new members in juntagrico to help them get started.

This is an extension for juntagrico. You can find more information about juntagrico here
(https://github.com/juntagrico/juntagrico)

## Installation


Install juntagrico-godparent via `pip`

    $ pip install juntagrico-godparent

or add it in your projects `requirements.txt`

In `settings.py` add `'juntagrico_godparent',`.

```python
INSTALLED_APPS = [
    ...
    'juntagrico',
    'juntagrico_godparent',
]
```

In your `urls.py` you also need to extend the pattern:

```python
urlpatterns = [
    ...
    path('', include('juntagrico_godparent.urls')),
]
```
