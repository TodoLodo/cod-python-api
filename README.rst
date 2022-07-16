.. toctree::

   intro
   All about strings <strings>
   datatypes

===================
**cod-python-api**
===================

.. image:: https://github.com/TodoLodo2089/cod-python-api/actions/workflows/tests.yml/badge.svg?branch=main
    :target: https://github.com/TodoLodo2089/cod-python-api.git

.. image:: https://badge.fury.io/py/cod-api.svg
    :target: https://badge.fury.io/py/cod-api

.. image:: https://badge.fury.io/gh/TodoLodo2089%2Fcod-python-api.svg
    :target: https://badge.fury.io/gh/TodoLodo2089%2Fcod-python-api

------------------------------------------------------------------------------------------------------------------------

**Call Of Duty API Library** for **python** with the implementation of both public and private API used by activision on
callofduty.com

====
Devs
====
`Todo Lodo`_ and `Engineer15`_

.. _Todo Lodo: https://github.com/TodoLodo2089
.. _Engineer15: https://github.com/Engineer152

=============
Documentation
=============
This package can be used directly as a python file or as a python library.

Installation
============

Install cod-api library using `pip`_:

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


.. _`logged in`:

Login with your sso token:

.. code-block:: python

    api.login('Your sso token')

Your sso token can be found by longing in at `callofduty`_, opening dev tools (ctr+shift+I), going to Applications >
Storage > Cookies > https://callofduty.com, filter to search 'ACT_SSO_COOKIE' and copy the value.

.. _callofduty: https://my.callofduty.com/

Game/Other sub classes
----------------------

Following importation and initiation of the class ``API``, its associated subclasses can be called by
``API.subClassName``.

Below are the available sub classes:

+-------------------+----------+
| sub class         | catogery |
+===================+==========+
|* `ColdWar`_       | game     |
+-------------------+----------+
|* `ModernWarfare`_ | game     |
+-------------------+----------+
|* `Vanguard`_      | game     |
+-------------------+----------+
|* `Warzone`_       | game     |
+-------------------+----------+
|* `Me`_            | other    |
+-------------------+----------+
|* `Misc`_          | other    |
+-------------------+----------+



For a detailed description, ``__doc__`` (docstring) of each sub class can be called as shown below:

.. _`ColdWar`:

``ColdWar``:

.. code-block:: python

    from cod_api import API

    api = API()

    # print out the docstring
    print(api.ColdWar.__doc__)

.. _`ModernWarfare`:

``ModernWarfare``:

.. code-block:: python

    from cod_api import API

    api = API()

    # print out the docstring
    print(api.ModernWarfare.__doc__)

.. _`Vanguard`:

``Vanguard``:

.. code-block:: python

    from cod_api import API

    api = API()

    # print out the docstring
    print(api.Vanguard.__doc__)

.. _`Warzone`:

``Warzone``:

.. code-block:: python

    from cod_api import API

    api = API()

    # print out the docstring
    print(api.Warzone.__doc__)

.. _`Me`:

``Me``:

.. code-block:: python

    from cod_api import API

    api = API()

    # print out the docstring
    print(api.Me.__doc__)

.. _`Misc`:

``Misc``:

.. code-block:: python

    from cod_api import API

    api = API()

    # print out the docstring
    print(api.Misc.__doc__)

Combat History
--------------

Any sub class of ``API``  that is of game catogery, has methods to check a player's combat history.
Note that before calling any sub class methods of ``API`` you must be `logged in`_.
Main methods are ``combatHistory()`` and ``combatHistoryWithDate()`` which are available for all ``ColdWar``,
``ModernWarfare``, ``Vanguard`` and ``Warzone`` classes.

The ``combatHistory()`` takes 2 input parameteres which are ``platform`` and ``gamertag`` of type `cod_api.platforms`_
and string respectively.

Here's an example for retrieving **Warzone** combat history of a player whose gamer tag is **Username#1234** on platform
**Battlenet**:

.. code-block:: python

    from cod_api import API, platforms

    # initiating the API class
    api = API()

    # loggin in with sso token
    api.login('your_sso_token')

    # retrieving combat history
    hist = api.Warzone.combatHistory(platforms.Battlenet, "Username#1234") # returns data of type dict

    # printing results to console
    print(hist)

The ``combatHistoryWithDate()`` takes 4 input parameteres which are ``platform``, ``gamertag``, ``start`` and ``end`` of
type `cod_api.platforms`_, string, int and int respectively.

``start`` and ``end`` parameters are utc timestamps in microseconds.

Here's an example for retrieving **ModernWarfare** combat history of a player whose gamer tag is **Username#1234567** on
platform **Activision** with in the timestamps **1657919309** (Friday, 15 July 2022 21:08:29) and **1657949309**
(Saturday, 16 July 2022 05:28:29):

.. code-block:: python

    from cod_api import API, platforms

    # initiating the API class
    api = API()

    # loggin in with sso token
    api.login('your_sso_token')

    # retrieving combat history
    hist = api.Warzone.combatHistoryWithDate(platforms.Activision, "Username#1234567", 1657919309, 1657949309) # returns data of type dict

    # printing results to console
    print(hist)

Additionally the methods ``breakdown()`` and ``breakdownWithDate()`` can be used to retrieve combat history without
details, where only the platform played on, game title, UTC timestamp, type ID, match ID and map ID is returned for
every match. And just like ``combatHistory()`` and ``combatHistoryWithDate()`` these methods are available for all
``ColdWar``, ``ModernWarfare``, ``Vanguard`` and ``Warzone`` classes.

The ``breakdown()`` takes 2 input parameteres which are ``platform`` and ``gamertag`` of type `cod_api.platforms`_ and
string respectively.

Here's an example for retrieving **Warzone** combat history breakdown of a player whose gamer tag is **Username#1234**
on platform **Battlenet**:

.. code-block:: python

    from cod_api import API, platforms

    # initiating the API class
    api = API()

    # loggin in with sso token
    api.login('your_sso_token')

    # retrieving combat history breakdown
    hist_b = api.Warzone.breakdown(platforms.Battlenet, "Username#1234") # returns data of type dict

    # printing results to console
    print(hist_b)

The ``breakdownWithDate()`` takes 4 input parameteres which are ``platform``, ``gamertag``, ``start`` and ``end`` of
type `cod_api.platforms`_, string, int and int respectively.

``start`` and ``end`` parameters are utc timestamps in microseconds.

Here's an example for retrieving **ModernWarfare** combat history breakdown of a player whose gamer tag is
**Username#1234567** on platform **Activision** with in the timestamps **1657919309** (Friday, 15 July 2022 21:08:29)
and **1657949309** (Saturday, 16 July 2022 05:28:29):

.. code-block:: python

    from cod_api import API, platforms

    # initiating the API class
    api = API()

    # loggin in with sso token
    api.login('your_sso_token')

    # retrieving combat history breakdown
    hist_b = api.Warzone.breakdownWithDate(platforms.Activision, "Username#1234567", 1657919309, 1657949309) # returns data of type dict

    # printing results to console
    print(hist_b)

Match Details
-------------

To retrieve details of a specific match, the method ``matchInfo()`` can be used and this is available for all
``ColdWar``, ``ModernWarfare``, ``Vanguard`` and ``Warzone`` classes. Details returned by this method contains
additional data than that of details returned by the methods ``combatHistory()`` and ``combatHistoryWithDate()`` for a
single match.

The ``matchInfo()`` takes 2 input parameteres which are ``platform`` and ``matchId`` of type `cod_api.platforms`_ and
integer respectively.

*Optionally the match ID can be retrieved during your gameplay where it will be visible on bottom left corner*

Here's an example for retrieving **Warzone** match details of a match where its id is **9484583876389482453**
on platform **Battlenet**:

.. code-block:: python

    from cod_api import API, platforms

    # initiating the API class
    api = API()

    # loggin in with sso token
    api.login('your_sso_token')

    # retrieving match details
    details = api.Warzone.matchInfo(platforms.Battlenet, 9484583876389482453) # returns data of type dict

    # printing results to console
    print(details)

Season Loot
-----------

Using the ``seasonLoot()``  method a player's obtained season loot can be retrieved for a specific game and this method
is available for ``ColdWar``, ``ModernWarfare`` and ``Vanguard`` classes.

The ``seasonLoot()`` takes 2 input parameteres which are ``platform`` and ``matchId`` of type `cod_api.platforms`_ and
integer respectively.

Here's an example for retrieving **ColdWar** season loot obtained by a player whose gamer tag is **Username#1234** on
platform **Battlenet**:

.. code-block:: python

    from cod_api import API, platforms

    # initiating the API class
    api = API()

    # loggin in with sso token
    api.login('your_sso_token')

    # retrieving season loot
    loot = api.ColdWar.seasonLoot(platforms.Battlenet, "Username#1234") # returns data of type dict)

    # printing results to console
    print(loot)

Map List
--------

Using the ``mapList()`` method all the maps and its available modes can be retrieved for a specific game. This method is
available for ``ColdWar``, ``ModernWarfare`` and ``Vanguard`` classes.

The ``mapList()`` takes 1 input parameteres which is ``platform`` of type `cod_api.platforms`_.

Here's an example for retrieving **Vanguard** map list and available modes respectively on platform PlayStation
(**PSN**):

.. code-block:: python

    from cod_api import API, platforms

    # initiating the API class
    api = API()

    # loggin in with sso token
    api.login('your_sso_token')

    # retrieving maps and respective modes available
    maps = api.Vanguard.mapList(platforms.PSN) # returns data of type dict)

    # printing results to console
    print(maps)

.. _cod_api.platforms:

platforms
---------

``platforms`` is an enum class available in ``cod_api`` which is used to specify the platform in certain method calls.

Available ``platforms`` are as follows:

+----------------------+----------------------------------------+
|Platform              | Remarks                                |
+======================+========================================+
|platforms.All         | All (no usage till further updates)    |
+----------------------+----------------------------------------+
|platforms.Activision  | Activision                             |
+----------------------+----------------------------------------+
|platforms.Battlenet   | Battlenet                              |
+----------------------+----------------------------------------+
|platforms.PSN         | PlayStation                            |
+----------------------+----------------------------------------+
|platforms.Steam       | Steam (no usage till further updates)  |
+----------------------+----------------------------------------+
|platforms.Uno         | Uno (activision unique id)             |
+----------------------+----------------------------------------+
|platforms.XBOX        | Xbox                                   |
+----------------------+----------------------------------------+

``platforms`` can be imported and used as follows:

.. code-block:: python

    from cod_api import platforms

    platforms.All        # All (no usage till further updates)

    platforms.Activision # Activision

    platforms.Battlenet  # Battlenet

    platforms.PSN        # PlayStation

    platforms.Steam      # Steam (no usage till further updates)

    platforms.Uno        # Uno (activision unique id)

    platforms.XBOX       # Xbox