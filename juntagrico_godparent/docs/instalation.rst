Installation
============

Basic Installation
------------------
Install juntagrico-godparent with :command:`pip`::

    $ pip install juntagrico-godparent

Django Setup
------------
You have to add the app to your installed apps in your Django settings

.. code-block:: python

    INSTALLED_APPS = [
        ...
        'juntagrico_godparent',
        'juntagrico',
    ]
    
And add the following at the end of your urls.py

.. code-block:: python

    path('', include('juntagrico_godparent.urls')),

Configuration
-------------

