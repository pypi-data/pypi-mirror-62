=============================
dj-mypypi
=============================

.. image:: https://badge.fury.io/py/dj-mypypi.svg
    :target: https://badge.fury.io/py/dj-mypypi

.. image:: https://travis-ci.org/kverdecia/dj-mypypi.svg?branch=master
    :target: https://travis-ci.org/kverdecia/dj-mypypi

.. image:: https://codecov.io/gh/kverdecia/dj-mypypi/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/kverdecia/dj-mypypi

This package provides a private python package index based on django

Documentation
-------------

The full documentation is at https://dj-mypypi.readthedocs.io.

Quickstart
----------

Install dj-mypypi::

    pip install dj-mypypi

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'djmypypi.apps.DjMyPypiConfig',
        ...
    )

Add dj-mypypi's URL patterns:

.. code-block:: python

    from djmypypi import urls as djmypypi_urls


    urlpatterns = [
        ...
        url(r'^', include(djmypypi_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
