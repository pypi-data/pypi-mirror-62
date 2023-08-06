========
Overview
========

When you need to make use of Paga Merchant Service API, using our libraries to interact with the APIs makes your
integration fast as most of the API logic has been handled when using the Paga Merchant Libraries

* Free software: MIT license

Installation
============

::

    pip install merchant_rest_service

You can also install the in-development version with::

    pip install git+ssh://git@https://github.com/pagadevcomm/merchant_rest_service.git/pagadevcomm/merchant_rest_service.git@master

Documentation
=============


To use the project:

.. code-block:: python

    import merchant_rest_service
    merchant_rest_service.longest()


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
