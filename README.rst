===================
**cod-python-api**
===================

.. meta::
    :description: Call Of Duty API Library for python with the implementation of both public and private API used by activision on callofduty.com
    :key: CallOfDuty API, CallOfDuty python API, CallOfDuty python

.. image:: https://github.com/TodoLodo/cod-python-api/actions/workflows/codeql-analysis.yml/badge.svg?branch=main
    :target: https://github.com/TodoLodo/cod-python-api.git

.. image:: https://img.shields.io/endpoint?url=https://cod-python-api.todolodo.xyz/stats?q=version
    :target: https://badge.fury.io/py/cod-api

.. image:: https://img.shields.io/endpoint?url=https://cod-python-api.todolodo.xyz/stats?q=downloads
    :target: https://badge.fury.io/gh/TodoLodo2089%2Fcod-python-api

------------------------------------------------------------------------------------------------------------------------

**Call Of Duty API Library** for **python** with the implementation of both public and private API used by activision on
callofduty.com

====
Devs
====
* `Todo Lodo`_ 
* `Engineer15`_

.. _Todo Lodo: https://todolodo.xyz
.. _Engineer15: https://github.com/Engineer152

============
Contributors
============
* `Werseter`_

.. _Werseter: https://github.com/Werseter

===============
Partnered Code
===============
`Node-CallOfDuty`_ by: `Lierrmm`_

.. _Node-CallOfDuty: https://github.com/Lierrmm/Node-CallOfDuty
.. _Lierrmm: https://github.com/Lierrmm

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
| sub class         | category |
+===================+==========+
|* `ColdWar`_       | game     |
+-------------------+----------+
|* `ModernWarfare`_ | game     |
+-------------------+----------+
|* `ModernWarfare2`_| game     |
+-------------------+----------+
|* `Vanguard`_      | game     |
+-------------------+----------+
|* `Warzone`_       | game     |
+-------------------+----------+
|* `Warzone2`_      | game     |
+-------------------+----------+
|* `Me`_            | other    |
+-------------------+----------+
|* `Shop`_          | other    |
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

.. _`ModernWarfare2`:

``ModernWarfare2``:

.. code-block:: python

    from cod_api import API

    api = API()

    # print out the docstring
    print(api.ModernWarfare2.__doc__)

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

.. _`Warzone2`:

``Warzone2``:

.. code-block:: python

    from cod_api import API

    api = API()

    # print out the docstring
    print(api.Warzone2.__doc__)

.. _`Me`:

``Me``:

.. code-block:: python

    from cod_api import API

    api = API()

    # print out the docstring
    print(api.Me.__doc__)

.. _`Shop`:

``Shop``:

.. code-block:: python

    from cod_api import API

    api = API()

    # print out the docstring
    print(api.Shop.__doc__)


.. _`Misc`:

``Misc``:

.. code-block:: python

    from cod_api import API

    api = API()

    # print out the docstring
    print(api.Misc.__doc__)

Full Profile History
--------------------

Any sub class of ``API``  that is of game category, has methods to check a player's combat history.
Note that before calling any sub class methods of ``API`` you must be `logged in`_.
Main method is ``fullData()`` and ``fullDataAsync()`` which is available for ``ColdWar``, ``ModernWarfare``,
``ModernWarfare2``, ``Vanguard``, ``Warzone`` and ``Warzone2`` classes.

Here's an example for retrieving **Warzone** full profile history of a player whose gamer tag is **Username#1234** on platform
**Battlenet**:

.. code-block:: python

    from cod_api import API, platforms
    import asyncio

    ## sync
    # initiating the API class
    api = API()

    # login in with sso token
    api.login('your_sso_token')

    # retrieving combat history
    profile = api.Warzone.fullData(platforms.Battlenet, "Username#1234") # returns data of type dict

    # printing results to console
    print(profile)

    ## async
    # in an async function
    async def example():
        # login in with sso token
        await api.loginAsync('your_sso_token')

        # retrieving combat history
        profile = await api.Warzone.fullDataAsync(platforms.Battlenet, "Username#1234") # returns data of type dict

        # printing results to console
        print(profile)

    # CALL THE example FUNCTION IN AN ASYNC ENVIRONMENT


Combat History
--------------

Main methods are ``combatHistory()`` and ``combatHistoryWithDate()`` for sync environments and ``combatHistoryAsync()``
and ``combatHistoryWithDateAsync()`` for async environments which are available for all ``ColdWar``, ``ModernWarfare``,
``ModernWarfare2``, ``Vanguard``, ``Warzone`` and ``Warzone2`` classes.

The ``combatHistory()`` and ``combatHistoryAsync()`` takes 2 input parameters which are ``platform`` and ``gamertag`` of
type `cod_api.platforms`_ and string respectively.

Here's an example for retrieving **Warzone** combat history of a player whose gamer tag is **Username#1234** on platform
**Battlenet**:

.. code-block:: python

    from cod_api import API, platforms

    # initiating the API class
    api = API()

    ## sync
    # login in with sso token
    api.login('your_sso_token')

    # retrieving combat history
    hist = api.Warzone.combatHistory(platforms.Battlenet, "Username#1234") # returns data of type dict

    # printing results to console
    print(hist)

    ## async
    # in an async function
    async def example():
        # login in with sso token
        await api.loginAsync('your_sso_token')

        # retrieving combat history
        hist = await api.Warzone.combatHistoryAsync(platforms.Battlenet, "Username#1234") # returns data of type dict

        # printing results to console
        print(hist)

    # CALL THE example FUNCTION IN AN ASYNC ENVIRONMENT

The ``combatHistoryWithDate()`` and ``combatHistoryWithDateAsync()`` takes 4 input parameters which are ``platform``,
``gamertag``, ``start`` and ``end`` of type `cod_api.platforms`_, string, int and int respectively.

``start`` and ``end`` parameters are utc timestamps in microseconds.

Here's an example for retrieving **ModernWarfare** combat history of a player whose gamer tag is **Username#1234567** on
platform **Activision** with in the timestamps **1657919309** (Friday, 15 July 2022 21:08:29) and **1657949309**
(Saturday, 16 July 2022 05:28:29):

.. code-block:: python

    from cod_api import API, platforms

    # initiating the API class
    api = API()

    ## sync
    # login in with sso token
    api.login('your_sso_token')

    # retrieving combat history
    hist = api.Warzone.combatHistoryWithDate(platforms.Activision, "Username#1234567", 1657919309, 1657949309) # returns data of type dict

    # printing results to console
    print(hist)
    
    ## async
    # in an async function
    async def example():
        # login in with sso token
        await api.loginAsync('your_sso_token')

        # retrieving combat history
        hist = await api.Warzone.combatHistoryWithDateAsync(platforms.Battlenet, "Username#1234", 1657919309, 1657949309) # returns data of type dict

        # printing results to console
        print(hist)

    # CALL THE example FUNCTION IN AN ASYNC ENVIRONMENT

Additionally the methods ``breakdown()`` and ``breakdownWithDate()`` for sync environments and ``breakdownAsync()`` and
``breakdownWithDateAsync()`` for async environments, can be used to retrieve combat history without details, where only
the platform played on, game title, UTC timestamp, type ID, match ID and map ID is returned for every match. These
methods are available for all ``ColdWar``, ``ModernWarfare``, ``ModernWarfare2``, ``Vanguard``, ``Warzone`` and
``Warzone2`` classes.

The ``breakdown()`` and `breakdownAsync()`` takes 2 input parameters which are ``platform`` and ``gamertag`` of type
`cod_api.platforms`_ and string respectively.

Here's an example for retrieving **Warzone** combat history breakdown of a player whose gamer tag is **Username#1234**
on platform **Battlenet**:

.. code-block:: python

    from cod_api import API, platforms

    # initiating the API class
    api = API()

    ## sync
    # login in with sso token
    api.login('your_sso_token')

    # retrieving combat history breakdown
    hist_b = api.Warzone.breakdown(platforms.Battlenet, "Username#1234") # returns data of type dict

    # printing results to console
    print(hist_b)

    ## async
    # in an async function
    async def example():
        # login in with sso token
        await api.loginAsync('your_sso_token')

        # retrieving combat history breakdown
        hist_b = await api.Warzone.breakdownAsync(platforms.Battlenet, "Username#1234") # returns data of type dict

        # printing results to console
        print(hist_b)

    # CALL THE example FUNCTION IN AN ASYNC ENVIRONMENT

The ``breakdownWithDate()`` and ``breakdownWithDateAsync()`` takes 4 input parameters which are ``platform``,
``gamertag``, ``start`` and ``end`` of type `cod_api.platforms`_, string, int and int respectively.

``start`` and ``end`` parameters are utc timestamps in microseconds.

Here's an example for retrieving **ModernWarfare** combat history breakdown of a player whose gamer tag is
**Username#1234567** on platform **Activision** with in the timestamps **1657919309** (Friday, 15 July 2022 21:08:29)
and **1657949309** (Saturday, 16 July 2022 05:28:29):

.. code-block:: python

    from cod_api import API, platforms

    # initiating the API class
    api = API()

    ## sync
    # login in with sso token
    api.login('your_sso_token')

    # retrieving combat history breakdown
    hist_b = api.Warzone.breakdownWithDate(platforms.Activision, "Username#1234567", 1657919309, 1657949309) # returns data of type dict

    # printing results to console
    print(hist_b)

    ## async
    # in an async function
    async def example():
        # login in with sso token
        await api.loginAsync('your_sso_token')

        # retrieving combat history breakdown
        hist_b = await api.Warzone.breakdownWithDateAsync(platforms.Activision, "Username#1234567", 1657919309, 1657949309) # returns data of type dict

        # printing results to console
        print(hist_b)

    # CALL THE example FUNCTION IN AN ASYNC ENVIRONMENT

Match Details
-------------

To retrieve details of a specific match, the method ``matchInfo()`` for sync environments and ``matchInfoAsync()`` for
async environments can be used. These methods are available for all ``ColdWar``, ``ModernWarfare``, ``ModernWarfare2``,
``Vanguard``, ``Warzone`` and ``Warzone2`` classes. Details returned by this method contains additional data than that
of details returned by the **combat history** methods for a single match.

The ``matchInfo()`` and ``matchInfoAsync()`` takes 2 input parameters which are ``platform`` and ``matchId`` of type
`cod_api.platforms`_ and integer respectively.

*Optionally the match ID can be retrieved during your gameplay where it will be visible on bottom left corner*

Here's an example for retrieving **Warzone** match details of a match where its id is **9484583876389482453**
on platform **Battlenet**:

.. code-block:: python

    from cod_api import API, platforms

    # initiating the API class
    api = API()

    ## sync
    # login in with sso token
    api.login('your_sso_token')

    # retrieving match details
    details = api.Warzone.matchInfo(platforms.Battlenet, 9484583876389482453) # returns data of type dict

    # printing results to console
    print(details)

    ## async
    # in an async function
    async def example():
        # login in with sso token
        await api.loginAsync('your_sso_token')

        # retrieving match details
        details = await api.Warzone.matchInfoAsync(platforms.Battlenet, 9484583876389482453) # returns data of type dict

        # printing results to console
        print(details)

    # CALL THE example FUNCTION IN AN ASYNC ENVIRONMENT

Season Loot
-----------

Using the ``seasonLoot()`` for sync environments and ``seasonLootAsync()`` for async environments, player's obtained
season loot can be retrieved for a specific game and this method is available for ``ColdWar``, ``ModernWarfare``,
``ModernWarfare2`` and ``Vanguard`` classes.

The ``seasonLoot()`` and ``seasonLootAsync()`` takes 2 input parameters which are ``platform`` and ``matchId`` of type
`cod_api.platforms`_ and integer respectively.

Here's an example for retrieving **ColdWar** season loot obtained by a player whose gamer tag is **Username#1234** on
platform **Battlenet**:

.. code-block:: python

    from cod_api import API, platforms

    # initiating the API class
    api = API()

    ## sync
    # login in with sso token
    api.login('your_sso_token')

    # retrieving season loot
    loot = api.ColdWar.seasonLoot(platforms.Battlenet, "Username#1234") # returns data of type dict)

    # printing results to console
    print(loot)

    ## async
    # in an async function
    async def example():
        # login in with sso token
        await api.loginAsync('your_sso_token')

        # retrieving season loot
        loot = await api.ColdWar.seasonLootAsync(platforms.Battlenet, "Username#1234") # returns data of type dict

        # printing results to console
        print(loot)

    # CALL THE example FUNCTION IN AN ASYNC ENVIRONMENT

Map List
--------

Using the ``mapList()`` for sync environments and ``mapListAsync()`` for async environments, all the maps and its
available modes can be retrieved for a specific game. These methods are available for ``ColdWar``, ``ModernWarfare``,
``ModernWarfare2`` and ``Vanguard`` classes.

The ``mapList()`` and ``mapListAsync()`` takes 1 input parameters which is ``platform`` of type `cod_api.platforms`_.

Here's an example for retrieving **Vanguard** map list and available modes respectively on platform PlayStation
(**PSN**):

.. code-block:: python

    from cod_api import API, platforms

    # initiating the API class
    api = API()

    ## sync
    # login in with sso token
    api.login('your_sso_token')

    # retrieving maps and respective modes available
    maps = api.Vanguard.mapList(platforms.PSN) # returns data of type dict

    # printing results to console
    print(maps)

    ## async
    # in an async function
    async def example():
        # login in with sso token
        await api.loginAsync('your_sso_token')

        # retrieving season loot
        maps = await api.Vanguard.mapListAsync(platforms.PSN) # returns data of type dict

        # printing results to console
        print(maps)

    # CALL THE example FUNCTION IN AN ASYNC ENVIRONMENT


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

User Info
----------

Using the ``info()`` method in sub class ``Me`` of ``API`` user information can be retrieved of the sso-token logged in
with

.. code-block:: python

    from cod_api import API

    # initiating the API class
    api = API()

    # login in with sso token
    api.login('your_sso_token')

    # retrieving user info
    userInfo = api.Me.info() # returns data of type dict

    # printing results to console
    print(userInfo)

User Friend Feed
----------------

Using the methods, ``friendFeed()`` for sync environments and ``friendFeedAsync()`` for async environments, in sub class
``Me`` of ``API``, user's friend feed can be retrieved of the sso-token logged in with

.. code-block:: python

    from cod_api import API

    # initiating the API class
    api = API()

    ## sync
    # login in with sso token
    api.login('your_sso_token')

    # retrieving user friend feed
    friendFeed = api.Me.friendFeed() # returns data of type dict

    # printing results to console
    print(friendFeed)
    
    ## async
    # in an async function
    async def example():
        # login in with sso token
        await api.loginAsync('your_sso_token')

        # retrieving user friend feed
        friendFeed = await api.Me.friendFeedAsync() # returns data of type dict

        # printing results to console
        print(friendFeed)

    # CALL THE example FUNCTION IN AN ASYNC ENVIRONMENT

User Event Feed
----------------

Using the methods ``eventFeed()`` for sync environments and ``eventFeedAsync()`` for async environments, in sub class
``Me`` of ``API`` user's event feed can be retrieved of the sso-token logged in with

.. code-block:: python

    from cod_api import API

    # initiating the API class
    api = API()

    ## sync
    # login in with sso token
    api.login('your_sso_token')

    # retrieving user event feed
    eventFeed = api.Me.eventFeed() # returns data of type dict

    # printing results to console
    print(eventFeed)

    ## async
    # in an async function
    async def example():
        # login in with sso token
        await api.loginAsync('your_sso_token')

        # retrieving user event feed
        eventFeed = await api.Me.eventFeedAsync() # returns data of type dict

        # printing results to console
        print(eventFeed)

    # CALL THE example FUNCTION IN AN ASYNC ENVIRONMENT

User Identities
----------------

Using the methods ``loggedInIdentities()`` for sync environments and ``loggedInIdentitiesAsync()`` for async
environments, in sub class ``Me`` of ``API`` user's identities can be retrieved of the sso-token logged in with

.. code-block:: python

    from cod_api import API

    # initiating the API class
    api = API()

    ## sync
    # login in with sso token
    api.login('your_sso_token')

    # retrieving user identities
    identities = api.Me.loggedInIdentities() # returns data of type dict

    # printing results to console
    print(identities)

    ## async
    # in an async function
    async def example():
        # login in with sso token
        await api.loginAsync('your_sso_token')

        # retrieving user identities
        identities = await api.Me.loggedInIdentitiesAsync() # returns data of type dict

        # printing results to console
        print(identities)

    # CALL THE example FUNCTION IN AN ASYNC ENVIRONMENT

User COD Points
----------------

Using the methods ``codPoints()`` for sync environments and ``codPointsAsync()`` for async environments, in sub class
``Me`` of ``API`` user's cod points can be retrieved of the sso-token logged in with

.. code-block:: python

    from cod_api import API

    # initiating the API class
    api = API()

    ## sync
    # login in with sso token
    api.login('your_sso_token')

    # retrieving user cod points
    cp = api.Me.codPoints() # returns data of type dict

    # printing results to console
    print(cp)

    ## async
    # in an async function
    async def example():
        # login in with sso token
        await api.loginAsync('your_sso_token')

        # retrieving user cod points
        cp = await api.Me.codPointsAsync() # returns data of type dict

        # printing results to console
        print(cp)

    # CALL THE example FUNCTION IN AN ASYNC ENVIRONMENT

User Accounts
----------------

Using the methods ``connectedAccounts()`` for sync environments and ``connectedAccountsAsync()`` for async environments,
in sub class ``Me`` of ``API`` user's connected accounts can be retrieved of the sso-token logged in with

.. code-block:: python

    from cod_api import API

    # initiating the API class
    api = API()

    ## sync
    # login in with sso token
    api.login('your_sso_token')

    # retrieving user connected accounts
    accounts = api.Me.connectedAccounts() # returns data of type dict

    # printing results to console
    print(accounts)

    ## async
    # in an async function
    async def example():
        # login in with sso token
        await api.loginAsync('your_sso_token')

        # retrieving user connected accounts
        accounts = await api.Me.connectedAccountsAsync() # returns data of type dict

        # printing results to console
        print(accounts)

    # CALL THE example FUNCTION IN AN ASYNC ENVIRONMENT

User settings
----------------

Using the methods ``settings()`` for sync environments and ``settingsAsync()`` for async environments, in sub class
``Me`` of ``API`` user's settings can be retrieved of the sso-token logged in with

.. code-block:: python

    from cod_api import API

    # initiating the API class
    api = API()

    ## sync
    # login in with sso token
    api.login('your_sso_token')

    # retrieving user settings
    settings = api.Me.settings() # returns data of type dict

    # printing results to console
    print(settings)

    ## async
    # in an async function
    async def example():
        # login in with sso token
        await api.loginAsync('your_sso_token')

        # retrieving user settings
        settings = await api.Me.settingsAsync() # returns data of type dict

        # printing results to console
        print(settings)

    # CALL THE example FUNCTION IN AN ASYNC ENVIRONMENT

-------------------------------------------------------------------------------------------------------------------------------

Donate
======

* `Donate Todo Lodo`_ 
* `Donate Engineer152`_
* `Donate Werseter`_

.. _Donate Todo Lodo: https://www.buymeacoffee.com/todolodo2089
.. _Donate Engineer152: https://www.paypal.com/paypalme/engineer15
.. _Donate Werseter: https://paypal.me/werseter
