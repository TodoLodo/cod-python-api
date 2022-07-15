==============
cod-python-api
==============

.. image:: https://github.com/TodoLodo2089/cod-python-api/actions/workflows/github-actions.yml/badge.svg?branch=main
    :target: https://github.com/TodoLodo2089/cod-python-api.git

.. image:: https://badge.fury.io/py/cod-api.svg
    :target: https://badge.fury.io/py/cod-api

**Call Of Duty API Library** for **python** with the implementation of both public and private API used by activision on 
callofduty.com

Devs
====
`Todo Lodo`_ and `Engineer15`_

.. _Todo Lodo: https://github.com/TodoLodo2089
.. _Engineer15: https://github.com/Engineer152

Documentation
=============
This package can be used directly as a python file or as a python library.

Installation
------------

Install cod-api library using `pip`_:

.. code-block:: bash

    pip install -U cod-api

.. _pip: https://pip.pypa.io/en/stable/getting-started/

Usage
-----

Initiation
~~~~~~~~~~

Import module with its classes:

.. code-block:: python

    from cod_api import API

    api = API()


Login with your sso token

.. code-block:: python

    api.login('Your sso token')

You sso token can be found by longing in at `callofduty`_, opening dev tools (ctr+shift+I),
going to Applications > Storage > Cookies > https://callofduty.com, filter to search 'ACT_SSO_COOKIE' and
copy the value

.. _callofduty: https://my.callofduty.com/

Game/Other sub classes
~~~~~~~~~~~~~~~~~~~~~~
Following importation and initiation of the class `API` its associated subclasses can be called by `API.subClassName`
and following are available sub classes

* `ColdWar`     - game
* `ModernWarfe` - game
* `Vanguard`    - game
* `Warzone`     - game
* `Me`          - other
* `Misc`        - other

To retrieve detailed description of each subclass `__doc__` (docstring) of each sub class can be called as shown below:

`ColdWar`

.. code-block:: python

    from cod_api import API

    api = API()

    # print out the docstring
    print(api.ColdWar)

`ModernWarfe`

.. code-block:: python

    from cod_api import API

    api = API()

    # print out the docstring
    print(api.ModernWarfare)

`Vanguard`

.. code-block:: python

    from cod_api import API

    api = API()

    # print out the docstring
    print(api.Vanguard)

`Warzone`

.. code-block:: python

    from cod_api import API

    api = API()

    # print out the docstring
    print(api.Warzone)

`Me`

.. code-block:: python

    from cod_api import API

    api = API()

    # print out the docstring
    print(api.Me)

`Misc`

.. code-block:: python

    from cod_api import API

    api = API()

    # print out the docstring
    print(api.Misc)
