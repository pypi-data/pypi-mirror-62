========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |requires|
        | |codecov|
        | |landscape|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/httpapi/badge/?style=flat
    :target: https://readthedocs.org/projects/httpapi
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.org/avengerpenguin/httpapi.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/avengerpenguin/httpapi

.. |requires| image:: https://requires.io/github/avengerpenguin/httpapi/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/avengerpenguin/httpapi/requirements/?branch=master

.. |codecov| image:: https://codecov.io/github/avengerpenguin/httpapi/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/avengerpenguin/httpapi

.. |landscape| image:: https://landscape.io/github/avengerpenguin/httpapi/master/landscape.svg?style=flat
    :target: https://landscape.io/github/avengerpenguin/httpapi/master
    :alt: Code Quality Status

.. |version| image:: https://img.shields.io/pypi/v/httpapi.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/httpapi

.. |wheel| image:: https://img.shields.io/pypi/wheel/httpapi.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/httpapi

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/httpapi.svg
    :alt: Supported versions
    :target: https://pypi.org/project/httpapi

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/httpapi.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/httpapi

.. |commits-since| image:: https://img.shields.io/github/commits-since/avengerpenguin/httpapi/v0.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/avengerpenguin/httpapi/compare/v0.0.0...master



.. end-badges

Pythonic helpers for HTTP APIs with long URLs.

Installation
============

::

    pip install httpapi

You can also install the in-development version with::

    pip install https://github.com/avengerpenguin/httpapi/archive/master.zip


Documentation
=============


https://httpapi.readthedocs.io/


Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
