__version__ = "2.0.1"

# Imports
import asyncio
import enum
import json
import uuid
from abc import abstractmethod
from datetime import datetime
from urllib.parse import quote

import aiohttp
import requests
from aiohttp import ClientResponseError


# Enums

class platforms(enum.Enum):
    All = 'all'
    Activision = 'acti'
    Battlenet = 'battle'
    PSN = 'psn'
    Steam = 'steam'
    Uno = 'uno'
    XBOX = 'xbl'


class games(enum.Enum):
    ColdWar = 'cw'
    ModernWarfare = 'mw'
    ModernWarfare2 = 'mw2'
    Vanguard = 'vg'
    Warzone = 'wz'
    Warzone2 = 'wz2'


class friendActions(enum.Enum):
    Invite = "invite"
    Uninvite = "uninvite"
    Remove = "remove"
    Block = "block"
    Unblock = "unblock"


class API:
    """
    Call Of Duty API Wrapper

    Developed by Todo Lodo & Engineer152

    Contributors
    - Werseter

    Source Code: https://github.com/TodoLodo/cod-python-api
    """
    def __init__(self):
        # sub classes
        self.Warzone = self.__WZ()
        self.ModernWarfare = self.__MW()
        self.Warzone2 = self.__WZ2()
        self.ModernWarfare2 = self.__MW2()
        self.ColdWar = self.__CW()
        self.Vanguard = self.__VG()
        self.Shop = self.__SHOP()
        self.Me = self.__USER()
        self.Misc = self.__ALT()

    async def loginAsync(self, sso_token: str) -> None:
        await API._Common.loginAsync(sso_token)

    # Login
    def login(self, ssoToken: str):
        API._Common.login(ssoToken)

    class _Common:
        requestHeaders = {
            "content-type": "application/json",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/74.0.3729.169 "
                          "Safari/537.36",
            "Accept": "application/json",
            "Connection": "Keep-Alive"
        }
        cookies = {"new_SiteId": "cod", "ACT_SSO_LOCALE": "en_US", "country": "US",
                   "ACT_SSO_COOKIE_EXPIRY": "1645556143194"}
        cachedMappings = None

        fakeXSRF = str(uuid.uuid4())
        baseUrl: str = "https://my.callofduty.com/api/papi-client"
        loggedIn: bool = False

        # endPoints

        # game platform lookupType gamertag type
        fullDataUrl = "/stats/cod/v1/title/%s/platform/%s/%s/%s/profile/type/%s"
        # game platform lookupType gamertag type start end [?limit=n or '']
        combatHistoryUrl = "/crm/cod/v2/title/%s/platform/%s/%s/%s/matches/%s/start/%d/end/%d/details"
        # game platform lookupType gamertag type start end
        breakdownUrl = "/crm/cod/v2/title/%s/platform/%s/%s/%s/matches/%s/start/%d/end/%d"
        # game platform lookupType gamertag
        seasonLootUrl = "/loot/title/%s/platform/%s/%s/%s/status/en"
        # game platform
        mapListUrl = "/ce/v1/title/%s/platform/%s/gameType/mp/communityMapData/availability"
        # game platform type matchId
        matchInfoUrl = "/crm/cod/v2/title/%s/platform/%s/fullMatch/%s/%d/en"

        @staticmethod
        async def loginAsync(sso_token: str) -> None:
            API._Common.cookies["ACT_SSO_COOKIE"] = sso_token
            API._Common.baseSsoToken = sso_token
            r = await API._Common.__Request(f"{API._Common.baseUrl}/crm/cod/v2/identities/{sso_token}")
            if r['status'] == 'success':
                API._Common.loggedIn = True
            else:
                raise InvalidToken(sso_token)

        @staticmethod
        def login(sso_token: str) -> None:
            API._Common.cookies["ACT_SSO_COOKIE"] = sso_token
            API._Common.baseSsoToken = sso_token

            r = requests.get(f"{API._Common.baseUrl}/crm/cod/v2/identities/{sso_token}",
                             headers=API._Common.requestHeaders, cookies=API._Common.cookies)

            if r.json()['status'] == 'success':
                API._Common.loggedIn = True
                API._Common.cookies.update(r.cookies)
            else:
                raise InvalidToken(sso_token)

        @staticmethod
        def sso_token() -> str:
            return API._Common.cookies["ACT_SSO_COOKIE"]

        # Requests

        @staticmethod
        async def __Request(url):
            async with aiohttp.client.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=True),
                                                    timeout=aiohttp.ClientTimeout(total=30)) as session:
                try:
                    async with session.get(url, cookies=API._Common.cookies,
                                           headers=API._Common.requestHeaders) as resp:
                        try:
                            resp.raise_for_status()
                        except ClientResponseError as err:
                            return {'status': 'error', 'data': {'type': type(err), 'message': err.message}}
                        else:
                            API._Common.cookies.update({c.key: c.value for c in session.cookie_jar})
                            return await resp.json()
                except asyncio.TimeoutError as err:
                    return {'status': 'error', 'data': {'type': type(err), 'message': str(err)}}

        async def __sendRequest(self, url: str):
            if self.loggedIn:
                response = await API._Common.__Request(f"{self.baseUrl}{url}")
                if response['status'] == 'success':
                    response['data'] = await self.__perform_mapping(response['data'])
                return response
            else:
                raise NotLoggedIn

        # client name url formatter
        def __cleanClientName(self, gamertag):
            return quote(gamertag.encode("utf-8"))

        # helper
        def __helper(self, platform, gamertag):
            lookUpType = "gamer"
            if platform == platforms.Uno:
                lookUpType = "id"
            if platform == platforms.Activision:
                platform = platforms.Uno
            if platform not in [platforms.Activision, platforms.Battlenet, platforms.Uno, platforms.All, platforms.PSN,
                                platforms.XBOX]:
                raise InvalidPlatform(platform)
            else:
                gamertag = self.__cleanClientName(gamertag)
            return lookUpType, gamertag, platform

        async def __get_mappings(self):
            if API._Common.cachedMappings is None:
                API._Common.cachedMappings = (
                    await API._Common.__Request('https://engineer152.github.io/wz-data/weapon-ids.json'),
                    await API._Common.__Request('https://engineer152.github.io/wz-data/game-modes.json'),
                    await API._Common.__Request('https://engineer152.github.io/wz-data/perks.json'))
            return API._Common.cachedMappings

        # mapping
        async def __perform_mapping(self, data):
            guns, modes, perks = await self.__get_mappings()
            if not isinstance(data, list) or 'matches' not in data:
                return data
            try:
                for match in data['matches']:
                    # time stamps
                    try:
                        match['utcStartDateTime'] = datetime.fromtimestamp(
                            match['utcStartSeconds']).strftime("%A, %B %d, %Y, %I:%M:%S")
                        match['utcEndDateTime'] = datetime.fromtimestamp(
                            match['utcEndSeconds']).strftime("%A, %B %d, %Y, %I:%M:%S")
                    except KeyError:
                        pass

                    # loadouts list
                    for loadout in match['player']['loadouts']:
                        # weapons
                        if loadout['primaryWeapon']['label'] is None:
                            try:
                                loadout['primaryWeapon']['label'] = guns[loadout['primaryWeapon']['name']]
                            except KeyError:
                                pass
                        if loadout['secondaryWeapon']['label'] is None:
                            try:
                                loadout['secondaryWeapon']['label'] = guns[loadout['secondaryWeapon']['name']]
                            except KeyError:
                                pass

                        # perks list
                        for perk in loadout['perks']:
                            if perk['label'] is None:
                                try:
                                    perk['label'] = perks[perk['name']]
                                except KeyError:
                                    pass

                        # extra perks list
                        for perk in loadout['extraPerks']:
                            if perk['label'] is None:
                                try:
                                    perk['label'] = perks[perk['name']]
                                except KeyError:
                                    pass

                    # loadout list
                    for loadout in match['player']['loadout']:
                        if loadout['primaryWeapon']['label'] is None:
                            try:
                                loadout['primaryWeapon']['label'] = guns[loadout['primaryWeapon']['name']]
                            except KeyError:
                                pass
                        if loadout['secondaryWeapon']['label'] is None:
                            try:
                                loadout['secondaryWeapon']['label'] = guns[loadout['secondaryWeapon']['name']]
                            except KeyError:
                                pass

                            # perks list
                            for perk in loadout['perks']:
                                if perk['label'] is None:
                                    try:
                                        perk['label'] = perks[perk['name']]
                                    except KeyError:
                                        pass

                            # extra perks list
                            for perk in loadout['extraPerks']:
                                if perk['label'] is None:
                                    try:
                                        perk['label'] = perks[perk['name']]
                                    except KeyError:
                                        pass
            except KeyError:
                pass

            # return mapped or unmapped data
            return data

        # API Requests
        async def _fullDataReq(self, game, platform, gamertag, type):
            lookUpType, gamertag, platform = self.__helper(platform, gamertag)
            return await self.__sendRequest(self.fullDataUrl % (game, platform.value, lookUpType, gamertag, type))

        async def _combatHistoryReq(self, game, platform, gamertag, type, start, end):
            lookUpType, gamertag, platform = self.__helper(platform, gamertag)
            return await self.__sendRequest(
                self.combatHistoryUrl % (game, platform.value, lookUpType, gamertag, type, start, end))

        async def _breakdownReq(self, game, platform, gamertag, type, start, end):
            lookUpType, gamertag, platform = self.__helper(platform, gamertag)
            return await self.__sendRequest(
                self.breakdownUrl % (game, platform.value, lookUpType, gamertag, type, start, end))

        async def _seasonLootReq(self, game, platform, gamertag):
            lookUpType, gamertag, platform = self.__helper(platform, gamertag)
            return await self.__sendRequest(self.seasonLootUrl % (game, platform.value, lookUpType, gamertag))

        async def _mapListReq(self, game, platform):
            return await self.__sendRequest(self.mapListUrl % (game, platform.value))

        async def _matchInfoReq(self, game, platform, type, matchId):
            return await self.__sendRequest(self.matchInfoUrl % (game, platform.value, type, matchId))

    class __GameDataCommons(_Common):
        """
        Methods
        =======
        Sync
        ----
        fullData(platform:platforms, gamertag:str)
            returns player's game data of type dict

        combatHistory(platform:platforms, gamertag:str)
            returns player's combat history of type dict

        combatHistoryWithDate(platform:platforms, gamertag:str, start:int, end:int)
            returns player's combat history within the specified timeline of type dict

        breakdown(platform:platforms, gamertag:str)
            returns player's combat history breakdown of type dict

        breakdownWithDate(platform:platforms, gamertag:str, start:int, end:int)
                    returns player's combat history breakdown within the specified timeline of type dict

        seasonLoot(platform:platforms, gamertag:str)
            returns player's season loot

        mapList(platform:platforms)
            returns available maps and available modes for each

        matchInfo(platform:platforms, matchId:int)
                    returns details match details of type dict

        Async
        ----
        fullDataAsync(platform:platforms, gamertag:str)
            returns player's game data of type dict

        combatHistoryAsync(platform:platforms, gamertag:str)
            returns player's combat history of type dict

        combatHistoryWithDateAsync(platform:platforms, gamertag:str, start:int, end:int)
            returns player's combat history within the specified timeline of type dict

        breakdownAsync(platform:platforms, gamertag:str)
            returns player's combat history breakdown of type dict

        breakdownWithDateAsync(platform:platforms, gamertag:str, start:int, end:int)
                    returns player's combat history breakdown within the specified timeline of type dict

        seasonLootAsync(platform:platforms, gamertag:str)
            returns player's season loot

        mapListAsync(platform:platforms)
            returns available maps and available modes for each

        matchInfoAsync(platform:platforms, matchId:int)
                    returns details match details of type dict
        """

        def __init_subclass__(cls, **kwargs):
            cls.__doc__ = cls.__doc__ + super(cls, cls).__doc__

        @property
        @abstractmethod
        def _game(self) -> str:
            raise NotImplementedError

        @property
        @abstractmethod
        def _type(self) -> str:
            raise NotImplementedError

        async def fullDataAsync(self, platform: platforms, gamertag: str):
            data = await self._fullDataReq(self._game, platform, gamertag, self._type)
            return data

        def fullData(self, platform: platforms, gamertag: str):
            return asyncio.run(self.fullDataAsync(platform, gamertag))

        async def combatHistoryAsync(self, platform: platforms, gamertag: str):
            data = await self._combatHistoryReq(self._game, platform, gamertag, self._type, 0, 0)
            return data

        def combatHistory(self, platform: platforms, gamertag: str):
            return asyncio.run(self.combatHistoryAsync(platform, gamertag))

        async def combatHistoryWithDateAsync(self, platform, gamertag: str, start: int, end: int):
            data = await self._combatHistoryReq(self._game, platform, gamertag, self._type, start, end)
            return data

        def combatHistoryWithDate(self, platform, gamertag: str, start: int, end: int):
            return asyncio.run(self.combatHistoryWithDateAsync(platform, gamertag, start, end))

        async def breakdownAsync(self, platform, gamertag: str):
            data = await self._breakdownReq(self._game, platform, gamertag, self._type, 0, 0)
            return data

        def breakdown(self, platform, gamertag: str):
            return asyncio.run(self.breakdownAsync(platform, gamertag))

        async def breakdownWithDateAsync(self, platform, gamertag: str, start: int, end: int):
            data = await self._breakdownReq(self._game, platform, gamertag, self._type, start, end)
            return data

        def breakdownWithDate(self, platform, gamertag: str, start: int, end: int):
            return asyncio.run(self.breakdownWithDateAsync(platform, gamertag, start, end))

        async def matchInfoAsync(self, platform, matchId: int):
            data = await self._matchInfoReq(self._game, platform, self._type, matchId)
            return data

        def matchInfo(self, platform, matchId: int):
            return asyncio.run(self.matchInfoAsync(platform, matchId))

        async def seasonLootAsync(self, platform, gamertag):
            data = await self._seasonLootReq(self._game, platform, gamertag)
            return data

        def seasonLoot(self, platform, gamertag):
            return asyncio.run(self.seasonLootAsync(platform, gamertag))

        async def mapListAsync(self, platform):
            data = await self._mapListReq(self._game, platform)
            return data

        def mapList(self, platform):
            return asyncio.run(self.mapListAsync(platform))
    # WZ

    class __WZ(__GameDataCommons):
        """
        Warzone class: A class to get players warzone stats, warzone combat history and specific warzone match details
            classCategory: game
            gameId/gameTitle: mw or wz
            gameType: wz

        """

        @property
        def _game(self) -> str:
            return "mw"

        @property
        def _type(self) -> str:
            return "wz"

        async def seasonLootAsync(self, platform, gamertag):
            raise InvalidEndpoint

        async def mapListAsync(self, platform):
            raise InvalidEndpoint

    # WZ2

    class __WZ2(__GameDataCommons):
        """
        Warzone 2 class: A class to get players warzone 2 stats, warzone 2 combat history and specific warzone 2 match details
            classCategory: game
            gameId/gameTitle: mw or wz
            gameType: wz2

        """

        @property
        def _game(self) -> str:
            return "mw2"

        @property
        def _type(self) -> str:
            return "wz2"

        async def seasonLootAsync(self, platform, gamertag):
            raise InvalidEndpoint

        async def mapListAsync(self, platform):
            raise InvalidEndpoint

    # MW

    class __MW(__GameDataCommons):
        """
        ModernWarfare class: A class to get players modernwarfare stats, modernwarfare combat history, a player's modernwarfare season loot, modernwarfare map list and specific modernwarfare match details
            classCategory: game
            gameId/gameTitle: mw
            gameType: mp

        """

        @property
        def _game(self) -> str:
            return "mw"

        @property
        def _type(self) -> str:
            return "mp"

    # CW

    class __CW(__GameDataCommons):
        """
         ColdWar class: A class to get players coldwar stats, coldwar combat history, a player's coldwar season loot, coldwar map list and specific coldwar match details
             classCategory: game
             gameId/gameTitle: cw
             gameType: mp

         """
        @property
        def _game(self) -> str:
            return "cw"

        @property
        def _type(self) -> str:
            return "mp"

    # VG

    class __VG(__GameDataCommons):
        """
         Vanguard class: A class to get players vanguard stats, vanguard combat history, a player's vanguard season loot, vanguard map list and specific vanguard match details
             classCategory: game
             gameId/gameTitle: vg
             gameType: pm

         """

        @property
        def _game(self) -> str:
            return "vg"

        @property
        def _type(self) -> str:
            return "mp"

    # MW2

    class __MW2(__GameDataCommons):
        """
        ModernWarfare 2 class: A class to get players modernwarfare 2 stats, modernwarfare 2 combat history, a player's modernwarfare 2 season loot, modernwarfare 2 map list and specific modernwarfare 2 match details
            classCategory: game
            gameId/gameTitle: mw
            gameType: mp

        """

        @property
        def _game(self) -> str:
            return "mw2"

        @property
        def _type(self) -> str:
            return "mp"

    # USER
    class __USER(_Common):
        def info(self):
            if self.loggedIn:
                rawData = requests.get(f"https://profile.callofduty.com/cod/userInfo/{self.sso_token()}",
                                       headers=API._Common.requestHeaders)
                rawData = json.loads(rawData.text.replace(
                    'userInfo(', '').replace(');', ''))

                data = {'userName': rawData['userInfo']['userName'], 'identities': []}
                for i in rawData['identities']:
                    data['identities'].append({
                        'platform': i['provider'],
                        'gamertag': i['username'],
                        'accountID': i['accountID']
                    })
                return data
            else:
                raise NotLoggedIn

        def __priv(self):
            d = self.info()
            return d['identities'][0]['platform'], quote(d['identities'][0]['gamertag'].encode("utf-8"))

        async def friendFeedAsync(self):
            p, g = self.__priv()
            data = await self._Common__sendRequest(
                    f"/userfeed/v1/friendFeed/platform/{p}/gamer/{g}/friendFeedEvents/en")
            return data

        def friendFeed(self):
            return asyncio.run(self.friendFeedAsync())

        async def eventFeedAsync(self):
            data = await self._Common__sendRequest(f"/userfeed/v1/friendFeed/rendered/en/{self.sso_token()}")
            return data

        def eventFeed(self):
            return asyncio.run(self.eventFeedAsync())

        async def loggedInIdentitiesAsync(self):
            data = await self._Common__sendRequest(f"/crm/cod/v2/identities/{self.sso_token()}")
            return data

        def loggedInIdentities(self):
            return asyncio.run(self.loggedInIdentitiesAsync())

        async def codPointsAsync(self):
            p, g = self.__priv()
            data = await self._Common__sendRequest(f"/inventory/v1/title/mw/platform/{p}/gamer/{g}/currency")
            return data

        def codPoints(self):
            return asyncio.run(self.codPointsAsync())

        async def connectedAccountsAsync(self):
            p, g = self.__priv()
            data = await self._Common__sendRequest(f"/crm/cod/v2/accounts/platform/{p}/gamer/{g}")
            return data

        def connectedAccounts(self):
            return asyncio.run(self.connectedAccountsAsync())

        async def settingsAsync(self):
            p, g = self.__priv()
            data = await self._Common__sendRequest(f"/preferences/v1/platform/{p}/gamer/{g}/list")
            return data

        def settings(self):
            return asyncio.run(self.settingsAsync())

    # SHOP
    class __SHOP(_Common):
        """
         Shop class: A class to get bundle details and battle pass loot
             classCategory: other

         Methods
         =======
         Sync
         ----
         purchasableItems(game: games)
             returns purchasable items for a specific gameId/gameTitle

         bundleInformation(game: games, bundleId: int)
             returns bundle details for the specific gameId/gameTitle and bundleId

         battlePassLoot(game: games, platform: platforms, season: int)
             returns battle pass loot for specific game and season on given platform

        Async
         ----
         purchasableItemsAsync(game: games)
             returns purchasable items for a specific gameId/gameTitle

         bundleInformationAsync(game: games, bundleId: int)
             returns bundle details for the specific gameId/gameTitle and bundleId

         battlePassLootAsync(game: games, platform: platforms, season: int)
             returns battle pass loot for specific game and season on given platform
         """

        async def purchasableItemsAsync(self, game: games):
            data = await self._Common__sendRequest(f"/inventory/v1/title/{game.value}/platform/uno/purchasable/public/en")
            return data

        def purchasableItems(self, game: games):
            return asyncio.run(self.purchasableItemsAsync(game))

        async def bundleInformationAsync(self, game: games, bundleId: int):
            data = await self._Common__sendRequest(f"/inventory/v1/title/{game.value}/bundle/{bundleId}/en")
            return data

        def bundleInformation(self, game: games, bundleId: int):
            return asyncio.run(self.bundleInformationAsync(game, bundleId))

        async def battlePassLootAsync(self, game: games, platform: platforms, season: int):
            data = await self._Common__sendRequest(
                f"/loot/title/{game.value}/platform/{platform.value}/list/loot_season_{season}/en")
            return data

        def battlePassLoot(self, game: games, platform: platforms, season: int):
            return asyncio.run(self.battlePassLootAsync(game, platform, season))

    # ALT
    class __ALT(_Common):

        async def searchAsync(self, platform, gamertag: str):
            lookUpType, gamertag, platform = self._Common__helper(platform, gamertag)
            data = await self._Common__sendRequest(f"/crm/cod/v2/platform/{platform.value}/username/{gamertag}/search")
            return data

        def search(self, platform, gamertag: str):
            return asyncio.run(self.searchAsync(platform, gamertag))


# Exceptions

class NotLoggedIn(Exception):
    def __str__(self):
        return "Not logged in!"


class InvalidToken(Exception):
    def __init__(self, token):
        self.token = token

    def __str__(self):
        return f"Token is invalid, token: {self.token}"


class InvalidPlatform(Exception):
    def __init__(self, platform: platforms):
        self.message: str
        if platform == platforms.Steam:
            self.message = "Steam cannot be used till further updates."
        else:
            self.message = "Invalid platform, use platform class!"


        super().__init__(self.message)

    def __str__(self):
        return self.message


class InvalidEndpoint(Exception):
    def __str__(self):
        return "This endpoint is not available for selected title"


class StatusError(Exception):
    def __str__(self):
        return "Status Error, Check if your sso token is valid or try again later."
