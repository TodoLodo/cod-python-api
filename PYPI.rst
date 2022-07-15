==============
cod-python-api
==============
**Call Of Duty API Library** for **python** with the implementation of both public and private API used by activision on 
callofduty.com

Devs
====
[Todo Lodo](https://github.com/TodoLodo2089) and [Engineer15](https://github.com/Engineer152)

Documentation
=============
This package can be used directly as a python file or as a python library.

Installation
------------

For direct use:

.. code-block:: bash

    git clone https://github.com/TodoLodo2089/cod-python-api.git

As a python library using `pip`_:

.. code-block:: bash

    pip install -U cod-api

.. _pip: https://pip.pypa.io/en/stable/getting-started/

Usage
=====

Initiation
----------

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

Retrieving game profile
-----------------------
A player's game profile can be retrieved by using API sub game classes with its function fullData(platform, gamertag)

*Example*:

.. code-block:: python

    from API import platforms

    profileData = api.ModernWarfare.fullData(platforms.Battlenet, "Username#1234")

*Output* > json

Retrieving combat history
-------------------------
A player's game profile can be retrieved by using API sub game classes with its functions combatHistory(platform, gamertag) or 
combatHistoryWithDate(platform, gamertag, start, end)

*Example*:

.. code-block:: python

    matchHistory = api.Warzone.combatHistory(platforms.Activision, "Username#123456")

*Output* > json