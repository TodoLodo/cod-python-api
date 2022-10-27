__version__ = "1.0.4"

# Imports
import asyncio
from datetime import datetime
import enum
import json
import requests
import sys
from urllib.parse import quote
import uuid


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
    def __init__(self):
        # common class
        self.__common = self.__common()

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

    # Login
    def login(self, ssoToken: str):
        try:
            self.__common.baseHeaders["__X-XSRF-TOKEN"] = self.__common.fakeXSRF
            self.__common.baseHeaders["__X-CSRF-TOKEN"] = self.__common.fakeXSRF
            self.__common.baseHeaders["Atvi-Auth"] = ssoToken
            self.__common.baseHeaders["ACT_SSO_COOKIE"] = ssoToken
            self.__common.baseHeaders["atkn"] = ssoToken
            self.__common.baseHeaders["cookie"] = f'{self.__common.baseCookie}' \
                                                  f'ACT_SSO_COOKIE={ssoToken};' \
                                                  f'XSRF-TOKEN={self.__common.fakeXSRF};' \
                                                  f'API_CSRF_TOKEN={self.__common.fakeXSRF};' \
                                                  f'ACT_SSO_EVENT="LOGIN_SUCCESS:1644346543228";' \
                                                  f'ACT_SSO_COOKIE_EXPIRY=1645556143194;' \
                                                  f'comid=cod;' \
                                                  f'ssoDevId=63025d09c69f47dfa2b8d5520b5b73e4;' \
                                                  f'tfa_enrollment_seen=true;' \
                                                  f'gtm.custom.bot.flag=human;'
            self.__common.baseSsoToken = ssoToken
            self.__common.basePostHeaders["__X-XSRF-TOKEN"] = self.__common.fakeXSRF
            self.__common.basePostHeaders["__X-CSRF-TOKEN"] = self.__common.fakeXSRF
            self.__common.basePostHeaders["Atvi-Auth"] = ssoToken
            self.__common.basePostHeaders["ACT_SSO_COOKIE"] = ssoToken
            self.__common.basePostHeaders["atkn"] = ssoToken
            self.__common.basePostHeaders["cookie"] = f'{self.__common.baseCookie}' \
                                                      f'ACT_SSO_COOKIE={ssoToken};' \
                                                      f'XSRF-TOKEN={self.__common.fakeXSRF};' \
                                                      f'API_CSRF_TOKEN={self.__common.fakeXSRF};' \
                                                      f'ACT_SSO_EVENT="LOGIN_SUCCESS:1644346543228";' \
                                                      f'ACT_SSO_COOKIE_EXPIRY=1645556143194;' \
                                                      f'comid=cod;' \
                                                      f'ssoDevId=63025d09c69f47dfa2b8d5520b5b73e4;' \
                                                      f'tfa_enrollment_seen=true;' \
                                                      f'gtm.custom.bot.flag=human;'

            r = requests.get(f"{self.__common.baseUrl}{self.__common.apiPath}/crm/cod/v2/identities/{ssoToken}",
                             headers=self.__common.baseHeaders)

            if r.json()['status'] == 'success':
                self.__common.loggedIn = True
                for sub in [self.Warzone, self.Warzone2, self.ModernWarfare, self.ModernWarfare2, self.ColdWar,
                            self.Vanguard, self.Shop, self.Me, self.Misc]:
                    sub.loggedIn = self.__common.loggedIn
                    sub.baseSsoToken = self.__common.baseSsoToken
                    sub.baseHeaders = self.__common.baseHeaders
                    sub.basePostHeaders = self.__common.basePostHeaders

                # deleting scope data
                del ssoToken, sub, r
            else:
                # delete scope data
                del ssoToken, r

                # system exit
                sys.exit(InvalidToken(ssoToken))
        except Exception as e:
            print(e)

            # delete scope data
            del ssoToken

            return e

    class __common:
        customHeaders: dict = {
            "__X-XSRF-TOKEN": str or None,
            "__X-CSRF-TOKEN": str or None,
            "Atvi-Auth": str or None,
            "ACT_SSO_COOKIE": str or None,
            "atkn": str or None,
            "cookie": str or None,
            "content-type": str or None,
        }
        customBody: dict = {}

        def __init__(self):
            # Variables

            # headers & cookies
            self.fakeXSRF = str(uuid.uuid4())
            self.userAgent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " \
                                  "AppleWebKit/537.36 (KHTML, like Gecko) " \
                                  "Chrome/74.0.3729.169 " \
                                  "Safari/537.36"
            self.baseCookie: str = "new_SiteId=cod;ACT_SSO_LOCALE=en_US;country=US;"
            self.baseSsoToken: str = ''
            self.baseUrl: str = "https://my.callofduty.com"
            self.apiPath: str = "/api/papi-client"
            self.loggedIn: bool = False

            # headers structures
            self.baseHeaders: API.customHeaders = {
                "content-type": 'application/json',
                "cookie": self.baseCookie,
                "user-agent": self.userAgent
            }

            self.basePostHeaders: API.customHeaders = {
                "content-type": 'text/plain',
                "cookie": self.baseCookie,
                "user-agent": self.userAgent
            }

            # endPoints

            # game platform lookupType gamertag type
            self.fullDataUrl = "/stats/cod/v1/title/%s/platform/%s/%s/%s/profile/type/%s"
            # game platform lookupType gamertag type start end [?limit=n or '']
            self.combatHistoryUrl = "/crm/cod/v2/title/%s/platform/%s/%s/%s/matches/%s/start/%d/end/%d/details"
            # game platform lookupType gamertag type start end
            self.breakdownUrl = "/crm/cod/v2/title/%s/platform/%s/%s/%s/matches/%s/start/%d/end/%d"
            # game platform lookupType gamertag
            self.seasonLootUrl = "/loot/title/%s/platform/%s/%s/%s/status/en"
            # game platform
            self.mapListUrl = "/ce/v1/title/%s/platform/%s/gameType/mp/communityMapData/availability"
            # game platform type matchId
            self.matchInfoUrl = "/crm/cod/v2/title/%s/platform/%s/fullMatch/%s/%d/en"

        # Requests
        async def __Request(self, method, url):
            h: self.customHeaders = self.customHeaders
            b: self.customBody = self.customBody
            if method == "GET":
                h = self.baseHeaders
            elif method == "POST":
                h = self.basePostHeaders

            try:
                r = requests.request(method=method, url=url, headers=h, data=b)

                # return data
                return r
            except Exception as e:

                return e

        async def __sendRequest(self, url: str):
            if self.loggedIn:
                respond = await self.__Request("GET", f"{self.baseUrl}{self.apiPath}{url}")
                if type(respond) != Exception:
                    if respond.status_code == 200:
                        data = respond.json()
                        if data['status'] == 'success':
                            data = self.__mapping(data['data'])
                            # delete scope data
                            del url, respond

                            # return data
                            return data
                        else:
                            # delete scope data
                            del url, respond

                            sys.exit(StatusError())
                    else:
                        # delete scope data
                        del url

                        return respond.status_code
            else:
                sys.exit(NotLoggedIn())

        async def __sendPostRequest(self, url: str, body: dict):
            if self.loggedIn:
                customBody = body
                respond = await self.__Request("POST", f"{self.baseUrl}{self.apiPath}{url}")
                if type(respond) != Exception:
                    if respond.status_code == 200:
                        return respond.json()
                    else:
                        return respond.status_code
            else:
                raise NotLoggedIn()

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
                if platform in [platforms.Activision, platforms.Battlenet, platforms.Uno]:
                    gamertag = self.__cleanClientName(gamertag)
            return lookUpType, gamertag, platform

        # mapping
        def __mapping(self, data):
            r = requests.get(
                'https://engineer152.github.io/wz-data/weapon-ids.json')
            guns = r.json()
            r = requests.get(
                'https://engineer152.github.io/wz-data/game-modes.json')
            modes = r.json()
            r = requests.get(
                'https://engineer152.github.io/wz-data/perks.json')
            perks = r.json()

            # guns
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
            except Exception as e:
                print(e)

            # delete scope data
            try:
                del guns, modes, perks, match, loadout, perk
            except UnboundLocalError:
                pass

            # return mapped or unmapped data
            return data

        # API Requests
        async def __fullDataReq(self, game, platform, gamertag, type):
            lookUpType, gamertag, platform = self.__helper(platform, gamertag)
            return await self.__sendRequest(self.fullDataUrl % (game, platform.value, lookUpType, gamertag, type))

        async def __combatHistoryReq(self, game, platform, gamertag, type, start, end):
            lookUpType, gamertag, platform = self.__helper(platform, gamertag)
            return await self.__sendRequest(self.combatHistoryUrl % (game, platform.value, lookUpType, gamertag, type, start, end))

        async def __breakdownReq(self, game, platform, gamertag, type, start, end):
            lookUpType, gamertag, platform = self.__helper(platform, gamertag)
            return await self.__sendRequest(self.breakdownUrl % (game, platform.value, lookUpType, gamertag, type, start, end))

        async def __seasonLootReq(self, game, platform, gamertag):
            lookUpType, gamertag, platform = self.__helper(platform, gamertag)
            return await self.__sendRequest(self.seasonLootUrl % (game, platform.value, lookUpType, gamertag))

        async def __mapListReq(self, game, platform):
            return await self.__sendRequest(self.mapListUrl % (game, platform.value))

        async def __matchInfoReq(self, game, platform, type, matchId):
            return await self.__sendRequest(self.matchInfoUrl % (game, platform.value, type, matchId))

    # WZ

    class __WZ(__common):
        """
        Warzone class: A class to get players warzone stats, warzone combat history and specific warzone match details
            classCatogery: game
            gameId/gameTitle: mw or wz
            gameType: wz

        Methods
        -------
        fullData(platform:platforms, gamertagLstr)
            returns player's game data of type dict

        combatHistory(platform:platforms, gamertag:str)
            returns player's combat history of type dict

        combatHistoryWithDate(platform:platforms, gamertag:str, start:int, end:int)
            returns player's combat history within the specified timeline of type dict

        breakdown(platform:platforms, gamertag:str)
            returns player's combat history breakdown of type dict

        breakdownWithDate(platform:platforms, gamertag:str, start:int, end:int)
                    returns player's combat history breakdown within the specified timeline of type dict

        matchInfo(platform:platforms, matchId:int)
                    returns details match details of type dict
        """

        def fullData(self, platform: platforms, gamertag: str):
            data = asyncio.run(self._common__fullDataReq(
                "mw", platform, gamertag, "wz"))
            return data

        def combatHistory(self, platform: platforms, gamertag: str):
            data = asyncio.run(self._common__combatHistoryReq(
                "mw", platform, gamertag, "wz", 0, 0))
            return data

        def combatHistoryWithDate(self, platform, gamertag: str, start: int, end: int):
            data = asyncio.run(self._common__combatHistoryReq(
                "mw", platform, gamertag, "wz", start, end))
            return data

        def breakdown(self, platform, gamertag: str):
            data = asyncio.run(self._common__breakdownReq(
                "mw", platform, gamertag, "wz", 0, 0))
            return data

        def breakdownWithDate(self, platform, gamertag: str, start: int, end: int):
            data = asyncio.run(self._common__breakdownReq(
                "mw", platform, gamertag, "wz", start, end))
            return data

        def matchInfo(self, platform, matchId: int):
            data = asyncio.run(self._common__matchInfoReq(
                "mw", platform, "wz", matchId))
            return data

    # WZ2

    class __WZ2(__common):
        """
        Warzone 2 class: A class to get players warzone 2 stats, warzone 2 combat history and specific warzone 2 match details
            classCatogery: game
            gameId/gameTitle: mw or wz
            gameType: wz2

        Methods
        -------
        fullData(platform:platforms, gamertagLstr)
            returns player's game data of type dict

        combatHistory(platform:platforms, gamertag:str)
            returns player's combat history of type dict

        combatHistoryWithDate(platform:platforms, gamertag:str, start:int, end:int)
            returns player's combat history within the specified timeline of type dict

        breakdown(platform:platforms, gamertag:str)
            returns player's combat history breakdown of type dict

        breakdownWithDate(platform:platforms, gamertag:str, start:int, end:int)
                    returns player's combat history breakdown within the specified timeline of type dict

        matchInfo(platform:platforms, matchId:int)
                    returns details match details of type dict
        """

        def fullData(self, platform: platforms, gamertag: str):
            data = asyncio.run(self._common__fullDataReq(
                "mw2", platform, gamertag, "wz2"))
            return data

        def combatHistory(self, platform: platforms, gamertag: str):
            data = asyncio.run(self._common__combatHistoryReq(
                "mw2", platform, gamertag, "wz2", 0, 0))
            return data

        def combatHistoryWithDate(self, platform, gamertag: str, start: int, end: int):
            data = asyncio.run(self._common__combatHistoryReq(
                "mw2", platform, gamertag, "wz2", start, end))
            return data

        def breakdown(self, platform, gamertag: str):
            data = asyncio.run(self._common__breakdownReq(
                "mw2", platform, gamertag, "wz2", 0, 0))
            return data

        def breakdownWithDate(self, platform, gamertag: str, start: int, end: int):
            data = asyncio.run(self._common__breakdownReq(
                "mw2", platform, gamertag, "wz2", start, end))
            return data

        def matchInfo(self, platform, matchId: int):
            data = asyncio.run(self._common__matchInfoReq(
                "mw2", platform, "wz2", matchId))
            return data

    # MW

    class __MW(__common):
        """
        ModernWarfare class: A class to get players modernwarfare stats, modernwarfare combat history, a player's modernwarfare season loot, modernwarfare map list and specific modernwarfare match details
            classCatogery: game
            gameId/gameTitle: mw
            gameType: mp

        Methods
        -------
        fullData(platform:platforms, gamertagLstr)
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
        """

        def fullData(self, platform, gamertag: str):
            data = asyncio.run(self._common__fullDataReq(
                "mw", platform, gamertag, "mp"))
            return data

        def combatHistory(self, platform, gamertag: str):
            data = asyncio.run(self._common__combatHistoryReq(
                "mw", platform, gamertag, "mp", 0, 0))
            return data

        def combatHistoryWithDate(self, platform, gamertag: str, start: int, end: int):
            data = asyncio.run(self._common__combatHistoryReq(
                "mw", platform, gamertag, "mp", start, end))
            return data

        def breakdown(self, platform, gamertag: str):
            data = asyncio.run(self._common__breakdownReq(
                "mw", platform, gamertag, "mp", 0, 0))
            return data

        def breakdownWithDate(self, platform, gamertag: str, start: int, end: int):
            data = asyncio.run(self._common__breakdownReq(
                "mw", platform, gamertag, "mp", start, end))
            return data

        def seasonLoot(self, platform, gamertag):
            data = asyncio.run(self._common__seasonLootReq(
                "mw", platform, gamertag))
            return data

        def mapList(self, platform):
            data = asyncio.run(self._common__mapListReq("mw", platform))
            return data

        def matchInfo(self, platform, matchId: int):
            data = asyncio.run(self._common__matchInfoReq(
                "mw", platform, "mp", matchId))
            return data

    # CW

    class __CW(__common):
        """
         ColdWar class: A class to get players coldwar stats, coldwar combat history, a player's coldwar season loot, coldwar map list and specific coldwar match details
             classCatogery: game
             gameId/gameTitle: cw
             gameType: mp

         Methods
         -------
         fullData(platform:platforms, gamertagLstr)
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
         """

        def fullData(self, platform, gamertag: str):
            data = asyncio.run(self._common__fullDataReq(
                "cw", platform, gamertag, "mp"))
            return data

        def combatHistory(self, platform, gamertag: str):
            data = asyncio.run(self._common__combatHistoryReq(
                "cw", platform, gamertag, "mp", 0, 0))
            return data

        def combatHistoryWithDate(self, platform, gamertag: str, start: int, end: int):
            data = asyncio.run(self._common__combatHistoryReq(
                "cw", platform, gamertag, "mp", start, end))
            return data

        def breakdown(self, platform, gamertag: str):
            data = asyncio.run(self._common__breakdownReq(
                "cw", platform, gamertag, "mp", 0, 0))
            return data

        def breakdownWithDate(self, platform, gamertag: str, start: int, end: int):
            data = asyncio.run(self._common__breakdownReq(
                "cw", platform, gamertag, "mp", start, end))
            return data

        def seasonLoot(self, platform, gamertag):
            data = asyncio.run(self._common__seasonLootReq(
                "cw", platform, gamertag))
            return data

        def mapList(self, platform):
            data = asyncio.run(self._common__mapListReq("cw", platform))
            return data

        def matchInfo(self, platform, matchId: int):
            data = asyncio.run(self._common__matchInfoReq(
                "cw", platform, "mp", matchId))
            return data

    # VG

    class __VG(__common):
        """
         Vanguard class: A class to get players vanguard stats, vanguard combat history, a player's vanguard season loot, vanguard map list and specific vanguard match details
             classCatogery: game
             gameId/gameTitle: vg
             gameType: pm

         Methods
         -------
         fullData(platform:platforms, gamertagLstr)
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
         """

        def fullData(self, platform, gamertag: str):
            data = asyncio.run(self._common__fullDataReq(
                "vg", platform, gamertag, "mp"))
            return data

        def combatHistory(self, platform, gamertag: str):
            data = asyncio.run(self._common__combatHistoryReq(
                "vg", platform, gamertag, "mp", 0, 0))
            return data

        def combatHistoryWithDate(self, platform, gamertag: str, start: int, end: int):
            data = asyncio.run(self._common__combatHistoryReq(
                "vg", platform, gamertag, "mp", start, end))
            return data

        def breakdown(self, platform, gamertag: str):
            data = asyncio.run(self._common__breakdownReq(
                "vg", platform, gamertag, "mp", 0, 0))
            return data

        def breakdownWithDate(self, platform, gamertag: str, start: int, end: int):
            data = asyncio.run(self._common__breakdownReq(
                "vg", platform, gamertag, "mp", start, end))
            return data

        def seasonLoot(self, platform, gamertag):
            data = asyncio.run(self._common__seasonLootReq(
                "vg", platform, gamertag))
            return data

        def mapList(self, platform):
            data = asyncio.run(self._common__mapListReq("vg", platform))
            return data

        def matchInfo(self, platform, matchId: int):
            data = asyncio.run(self._common__matchInfoReq(
                "vg", platform, "mp", matchId))
            return data

    # MW2

    class __MW2(__common):
        """
        ModernWarfare 2 class: A class to get players modernwarfare 2 stats, modernwarfare 2 combat history, a player's modernwarfare 2 season loot, modernwarfare 2 map list and specific modernwarfare 2 match details
            classCatogery: game
            gameId/gameTitle: mw
            gameType: mp

        Methods
        -------
        fullData(platform:platforms, gamertagLstr)
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
        """

        def fullData(self, platform, gamertag: str):
            data = asyncio.run(self._common__fullDataReq(
                "mw2", platform, gamertag, "mp"))
            return data

        def combatHistory(self, platform, gamertag: str):
            data = asyncio.run(self._common__combatHistoryReq(
                "mw2", platform, gamertag, "mp", 0, 0))
            return data

        def combatHistoryWithDate(self, platform, gamertag: str, start: int, end: int):
            data = asyncio.run(self._common__combatHistoryReq(
                "mw2", platform, gamertag, "mp", start, end))
            return data

        def breakdown(self, platform, gamertag: str):
            data = asyncio.run(self._common__breakdownReq(
                "mw2", platform, gamertag, "mp", 0, 0))
            return data

        def breakdownWithDate(self, platform, gamertag: str, start: int, end: int):
            data = asyncio.run(self._common__breakdownReq(
                "mw2", platform, gamertag, "mp", start, end))
            return data

        def seasonLoot(self, platform, gamertag):
            data = asyncio.run(self._common__seasonLootReq(
                "mw2", platform, gamertag))
            return data

        def mapList(self, platform):
            data = asyncio.run(self._common__mapListReq("mw2", platform))
            return data

        def matchInfo(self, platform, matchId: int):
            data = asyncio.run(self._common__matchInfoReq(
                "mw2", platform, "mp", matchId))
            return data

    # USER
    class __USER(__common):
        def info(self):
            if self.loggedIn:
                headers = self.baseHeaders
                headers['Accept'] = 'application/json'
                rawData = requests.get(
                    f"https://profile.callofduty.com/cod/userInfo/{self.baseSsoToken}", headers=headers)
                rawData = json.loads(rawData.text.replace(
                    'userInfo(', '').replace(');', ''))

                data = {
                    'userName': rawData['userInfo']['userName']
                }
                data['identities'] = []
                for i in rawData['identities']:
                    data['identities'].append({
                        'platform': i['provider'],
                        'gamertag': i['username'],
                        'accountID': i['accountID']
                    })
                return data
            else:
                sys.exit(NotLoggedIn())

        def __priv(self):
            d = self.info()
            return d['identities'][0]['platform'], quote(d['identities'][0]['gamertag'].encode("utf-8"))

        def friendFeed(self):
            p, g = self.__priv()
            data = asyncio.run(
                self._common__sendRequest(
                    f"/userfeed/v1/friendFeed/platform/{p}/gamer/{g}/friendFeedEvents/en")
            )
            return data

        def eventFeed(self):
            data = asyncio.run(self._common__sendRequest(
                f"/userfeed/v1/friendFeed/rendered/en/{self.baseSsoToken}"))
            return data

        def loggedInIdentities(self):
            data = asyncio.run(self._common__sendRequest(
                f"/crm/cod/v2/identities/{self.baseSsoToken}"))
            return data

        def codPoints(self):
            p, g = self.__priv()
            data = asyncio.run(self._common__sendRequest(
                f"/inventory/v1/title/mw/platform/{p}/gamer/{g}/currency"))
            return data

        def connectedAccounts(self):
            p, g = self.__priv()
            data = asyncio.run(self._common__sendRequest(
                f"/crm/cod/v2/accounts/platform/{p}/gamer/{g}"))
            return data

        def settings(self):
            p, g = self.__priv()
            data = asyncio.run(self._common__sendRequest(
                f"/preferences/v1/platform/{p}/gamer/{g}/list"))
            return data

    # SHOP
    class __SHOP(__common):
        """
         Shop class: A class to get bundle details and battle pass loot
             classCatogery: other

         Methods
         -------
         purchasableItems(game: games)
             returns purchasable items for a specific gameId/gameTitle

         bundleInformation(game: games, bundleId: int)
             returns bundle details for the specific gameId/gameTitle and bundleId

         battlePassLoot(game: games, platform: platforms, season: int)
             returns battle pass loot for specific game and season on given platform
         """

        def purchasableItems(self, game: games):
            data = asyncio.run(
                self._common__sendRequest(f"/inventory/v1/title/{game}/platform/uno/purchasable/public/en"))
            return data

        def bundleInformation(self, game: games, bundleId: int):
            data = asyncio.run(self._common__sendRequest(
                f"/inventory/v1/title/{game}/bundle/{bundleId}/en"))

        def battlePassLoot(self, game: games, platform: platforms, season: int):
            data = asyncio.run(self._common__sendRequest(
                f"/loot/title/{game}/platform/{platform.value}/list/loot_season_{season}/en"))
            return data

    # ALT
    class __ALT(__common):

        def search(self, platform, gamertag: str):
            lookUpType, gamertag, platform = self._common__helper(platform, gamertag)
            data = asyncio.run(self._common__sendRequest(
                f"/crm/cod/v2/platform/{platform.value}/username/{gamertag}/search"))
            return data


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

    def __str__(self):
        return self.message


class StatusError(Exception):
    def __str__(self):
        return "Status Error, Check if your sso token is valid or try again later."
