==============
cod-python-api
==============

.. image:: https://github.com/TodoLodo2089/cod-python-api/actions/workflows/tests.yml/badge.svg?branch=main
    :target: https://github.com/TodoLodo2089/cod-python-api.git

.. image:: https://badge.fury.io/py/cod-api.svg
    :target: https://badge.fury.io/py/cod-api

.. image:: https://badge.fury.io/gh/TodoLodo2089%2Fcod-python-api.svg
    :target: https://badge.fury.io/gh/TodoLodo2089%2Fcod-python-api

------------------------------------------------------------------------------------------------------------------------

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


.. _`logged in`:

Login with your sso token

.. code-block:: python

    api.login('Your sso token')

You sso token can be found by longing in at `callofduty`_, opening dev tools (ctr+shift+I),
going to Applications > Storage > Cookies > https://callofduty.com, filter to search 'ACT_SSO_COOKIE' and
copy the value

.. _callofduty: https://my.callofduty.com/

Game/Other sub classes
~~~~~~~~~~~~~~~~~~~~~~
Following importation and initiation of the class ``API`` its associated subclasses can be called by ``API.subClassName``
and following are available sub classes

+-----------------+----------+
| sub class       | catogery |
+=================+==========+
|* `ColdWar`_     | game     |
+-----------------+----------+
|* `ModernWarfe`_ | game     |
+-----------------+----------+
|* `Vanguard`_    | game     |
+-----------------+----------+
|* `Warzone`_     | game     |
+-----------------+----------+
|* `Me`_          | other    |
+-----------------+----------+
|* `Misc`_        | other    |
+-----------------+----------+



For a detailed description of each subclass, `__doc__` (docstring) of each sub class can be called as shown below:

.. _ColdWar: _`ColdWa`

.. _`ColdWa`:

`ColdWar`

.. code-block:: python

    from cod_api import API

    api = API()

    # print out the docstring
    print(api.ColdWar.__doc__)

.. _`ModernWarfe`:

`ModernWarfe`

.. code-block:: python

    from cod_api import API

    api = API()

    # print out the docstring
    print(api.ModernWarfare.__doc__)

.. _`Vanguard`:

`Vanguard`

.. code-block:: python

    from cod_api import API

    api = API()

    # print out the docstring
    print(api.Vanguard.__doc__)

.. _`Warzone`:

`Warzone`

.. code-block:: python

    from cod_api import API

    api = API()

    # print out the docstring
    print(api.Warzone.__doc__)

.. _`Me`:

`Me`

.. code-block:: python

    from cod_api import API

    api = API()

    # print out the docstring
    print(api.Me.__doc__)

.. _`Misc`:

`Misc`

.. code-block:: python

    from cod_api import API

    api = API()

    # print out the docstring
    print(api.Misc.__doc__)

Combat History
~~~~~~~~~~~~~~

Any sub class of ``API``  of catogery game has methods to check a player's combat history.
Note that before calling any methods of sub classes of ``API`` you must be `logged in`_.
Main methods are ``combatHistory()`` and ``combatHistoryWithDate()`` which is available for `C`