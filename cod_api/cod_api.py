# Imports
import asyncio
import enum
import requests
from urllib.parse import quote
import uuid

# Enums
class platforms(enum.Enum):
    All = 'all'
    Activision = 'uno'
    Battlenet = 'battle'
    PSN = 'psn'
    Steam = 'steam'
    Uno = 'uno'
    XBOX = 'xbl'


class games(enum.Enum):
    ColdWar = 'cw'
    ModernWarfare = 'mw'
    Vanguard = 'vg'
    Warzone = 'wz'


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
        self.ColdWar = self.__CW()
        self.Vanguard = self.__VG()
        self.Shop = self.__SHOP()
        self.Me = self.__USER()
        self.Misc = self.__ALT()

    # Login
    def login(self, ssoToken: str):
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
        self.__common.loggedIn = True

        for sub in [self.Warzone, self.ModernWarfare, self.ColdWar, self.Vanguard, self.Shop, self.Me, self.Misc]:
            sub.loggedIn = self.__common.loggedIn
            sub.baseSsoToken = self.__common.baseSsoToken
            sub.baseHeaders = self.__common.baseHeaders
            sub.basePostHeaders = self.__common.basePostHeaders


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
            self.userAgent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
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
                return r
            except Exception as e:
                return e

        async def __sendRequest(self, url: str):
            if self.loggedIn:
                respond = await self.__Request("GET", f"{self.baseUrl}{self.apiPath}{url}")
                if type(respond) != Exception:
                    if respond.status_code == 200:
                        return respond.json()
                    else:
                        return respond.status_code

        async def __sendPostRequest(self, url: str, body: dict):
            if self.loggedIn:
                customBody = body
                respond = await self.__Request("POST", f"{self.baseUrl}{self.apiPath}{url}")
                if type(respond) != Exception:
                    if respond.status_code == 200:
                        return respond.json()
                    else:
                        return respond.status_code

        # client name url formatter
        def __cleanClientName(self, ganertage):
            return quote(ganertage.encode("utf-8"))

        # helper
        def __helper(self, platform, gamertag):
            lookUpType = "id" if platform == platforms.Uno else "gamer"
            if platform not in [platforms.Activision, platforms.Battlenet, platforms.Uno, platforms.All, platforms.PSN,
                                platforms.XBOX]:
                raise InvalidPlatform(platform)
            else:
                if platform in [platforms.Activision, platforms.Battlenet, platforms.Uno]:
                    gamertag = self.__cleanClientName(gamertag)
            return lookUpType, gamertag

        # API Requests
        async def __fullDataReq(self, game, platform, gamertag, type):
            lookUpType, gamertag = self.__helper(platform, gamertag)
            return await self.__sendRequest(self.fullDataUrl % (game, platform.value, lookUpType, gamertag, type))

        async def __combatHistoryReq(self, game, platform, gamertag, type, start, end):
            lookUpType, gamertag = self.__helper(platform, gamertag)
            return await self.__sendRequest(self.combatHistoryUrl % (game, platform.value, lookUpType, gamertag, type, start, end))

        async def __breakdownReq(self, game, platform, gamertag, type, start, end):
            lookUpType, gamertag = self.__helper(platform, gamertag)
            return await self.__sendRequest(self.breakdownUrl % (game, platform.value, lookUpType, gamertag, type, start, end))

        async def __seasonLootReq(self, game, platform, gamertag):
            lookUpType, gamertag = self.__helper(platform, gamertag)
            return await self.__sendRequest(self.seasonLootUrl % (game, platform.value, lookUpType, gamertag))

        async def __mapListReq(self, game, platform):
            return await self.__sendRequest(self.mapListUrl % (game, platform.value))

        async def __matchInforReq(self, game, platform, type, matchId):
            return await self.__sendRequest(self.matchInfoUrl % (game, platform.value, type, matchId))


    # WZ
    class __WZ(__common):
        """
        Warzone class: A class to get players warzone stats

        Methods
        -------
        fullData(platform:platforms, gamertagLstr)
            returns player's game data of type dict

        combatHistory(platform:platforms, gamertag:str)
            returns player's combat history of type dict

        combatHistoryWithDate(platform:platforms, gamertag:str, start:int, end:int)
            returns player's combat history within the specified timeline of type dict
        """

        async def fullData(self, platform:platforms, gamertag: str):
            data = await self.__fullDataReq("mw", platform, gamertag, "wz")
            return data

        async def combatHistory(self, platform: platforms, gamertag: str):
            data = await self._common__combatHistoryReq("mw", platform, gamertag, "wz", 0, 0)
            return data

        async def combatHistoryWithDate(self, platform, gamertag: str, start:int, end:int):
            data = await self.__combatHistoryReq("mw", platform, gamertag, "wz", start, end)
            return data

        async def breakdown(self, platform, gamertag: str):
            data = await self.__breakdownReq("mw", platform, gamertag, "wz", 0, 0)
            return data

        async def breakdownWithDate(self, platform, gamertag: str, start:int, end:int):
            data = await self.__breakdownReq("mw", platform, gamertag, "wz", start, end)
            return data

        async def matchInfo(self, platform, matchId:int):
            data = await self.__matchInforReq("mw", platform, "wz", matchId)
            return data


    # MW
    class __MW(__common):
        async def fullData(self, platform, gamertag: str):
            data = await self.__fullDataReq("mw", platform, gamertag, "mp")
            return data

        async def combatHistory(self, platform, gamertag: str):
            data = await self.__combatHistoryReq("mw", platform, gamertag, "mp", 0, 0)
            return data

        async def combatHistoryWithDate(self, platform, gamertag: str, start: int, end: int):
            data = await self.__combatHistoryReq("mw", platform, gamertag, "mp", start, end)
            return data

        async def breakdown(self, platform, gamertag: str):
            data = await self.__breakdownReq("mw", platform, gamertag, "mp", 0, 0)
            return data

        async def breakdownWithDate(self, platform, gamertag: str, start: int, end: int):
            data = await self.__breakdownReq("mw", platform, gamertag, "mp", start, end)
            return data

        async def seasonLoot(self, platform, gamertag):
            data = await self.__seasonLootReq("mw", platform, gamertag)
            return data

        async def mapList(self, platform):
            data = await self.__mapListReq("mw", platform)
            return data

        async def matchInfo(self, platform, matchId: int):
            data = await self.__matchInforReq("mw", platform, "mp", matchId)
            return data


    # CW
    class __CW(__common):
        async def fullData(self, platform, gamertag: str):
            data = await self.__fullDataReq("cw", platform, gamertag, "mp")
            return data

        async def combatHistory(self, platform, gamertag: str):
            data = await self.__combatHistoryReq("cw", platform, gamertag, "mp", 0, 0)
            return data

        async def combatHistoryWithDate(self, platform, gamertag: str, start: int, end: int):
            data = await self.__combatHistoryReq("cw", platform, gamertag, "mp", start, end)
            return data

        async def breakdown(self, platform, gamertag: str):
            data = await self.__breakdownReq("cw", platform, gamertag, "mp", 0, 0)
            return data

        async def breakdownWithDate(self, platform, gamertag: str, start: int, end: int):
            data = await self.__breakdownReq("cw", platform, gamertag, "mp", start, end)
            return data

        async def seasonLoot(self, platform, gamertag):
            data = await self.__seasonLootReq("cw", platform, gamertag)
            return data

        async def mapList(self, platform):
            data = await self.__mapListReq("cw", platform)
            return data

        async def matchInfo(self, platform, matchId: int):
            data = await self.__matchInforReq("cw", platform, "mp", matchId)
            return data


    # VG
    class __VG(__common):
        async def fullData(self, platform, gamertag: str):
            data = await self.__fullDataReq("vg", platform, gamertag, "mp")
            return data

        async def combatHistory(self, platform, gamertag: str):
            data = await self.__combatHistoryReq("vg", platform, gamertag, "mp", 0, 0)
            return data

        async def combatHistoryWithDate(self, platform, gamertag: str, start: int, end: int):
            data = await self.__combatHistoryReq("vg", platform, gamertag, "mp", start, end)
            return data

        async def breakdown(self, platform, gamertag: str):
            data = await self.__breakdownReq("vg", platform, gamertag, "mp", 0, 0)
            return data

        async def breakdownWithDate(self, platform, gamertag: str, start: int, end: int):
            data = await self.__breakdownReq("vg", platform, gamertag, "mp", start, end)
            return data

        async def seasonLoot(self, platform, gamertag):
            data = await self.__seasonLootReq("vg", platform, gamertag)
            return data

        async def mapList(self, platform):
            data = await self.__mapListReq("vg", platform)
            return data

        async def matchInfo(self, platform, matchId: int):
            data = await self.__matchInforReq("vg", platform, "mp", matchId)
            return data


    # SHOP
    class __SHOP(__common):
        async def purchasableItems(self, game: str):
            data = await self.__sendRequest(f"/inventory/v1/title/{game}/platform/psn/purchasable/public/en")
            return data

        async def bundleInformation(self, game: str, bundleId):
            data = await self.__sendRequest(f"/inventory/v1/title/{game}/bundle/${bundleId}/en")

        async def battlePassLoot(self, platform, season:int):
            data = await self.__sendRequest(f"/loot/title/mw/platform/{platform.value}/list/loot_season_{season}/en")
            return data


    # USER
    class __USER(__common):
        async def friendFeed(self, platform, gamertag:str):
            lookUpType, gamertag = self.__helper(platform, gamertag)
            data = await self.__sendRequest(f"/userfeed/v1/friendFeed/platform/{platform.value}/gamer/{gamertag}/friendFeedEvents/en")
            return data

        async def eventFeed(self):
            data = await self.__sendRequest(f"/userfeed/v1/friendFeed/rendered/en/{self.baseSsoToken}")
            return data

        async def loggedInIdentities(self):
            data = await self.__sendRequest(f"/crm/cod/v2/identities/{self.baseSsoToken}")
            return data

        async def codPoints(self, platform, gamertag:str):
            lookUpType, gamertag = self.__helper(platform, gamertag)
            data = await self.__sendRequest(f"/inventory/v1/title/mw/platform/{platform.value}/gamer/{gamertag}/currency")
            return data

        async def connectedAccounts(self, platform, gamertag:str):
            lookUpType, gamertag = self.__helper(platform, gamertag)
            data = await self.__sendRequest(f"/crm/cod/v2/accounts/platform/{platform.value}/{lookUpType}/{gamertag}")
            return data

        async def settings(self, platform, gamertag:str):
            lookUpType, gamertag = self.__helper(platform, gamertag)
            data = await self.__sendRequest(f"/preferences/v1/platform/{platform.value}/gamer/{gamertag}/list")
            return data


    # ALT
    class __ALT(__common):
        async def search(self, platform, gamertag:str):
            lookUpType, gamertag = self.__helper(platform, gamertag)
            data = await self.sendRequest(f"/crm/cod/v2/platform/{platform.value}/username/{gamertag}/search")
            return data


class NotLoggedIn(Exception):
    def __str__(self):
        return "Not logged in!"


class InvalidPlatform(Exception):
    def __init__(self, platform: platforms):
        self.message: str
        if platform == platforms.Steam:
            self.message = "Steam Doesn't exist for MW. Try `battle` instead."
        else:
            self.message = f"Invalid platform, use platform class!"

    def __str__(self):
        return self.message
