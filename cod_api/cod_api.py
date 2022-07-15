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


class __main__:
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
        h: API.customHeaders = API.customHeaders
        b: API.customBody = API.customBody
        if method == "GET":
            h = self.baseHeaders
        elif method == "POST":
            h = self.basePostHeaders

        try:
            r = requests.request(method=method, url=url, headers=h, data=b)
            return r
        except Exception as e:
            return e

    async def sendRequest(self, url: str):
        if self.loggedIn:
            respond = await self.__Request("GET", f"{self.baseUrl}{self.apiPath}{url}")
            if type(respond) != Exception:
                if respond.status_code == 200:
                    return respond.json()
                else:
                    return respond.status_code

    async def sendPostRequest(self, url: str, body: dict):
        if self.loggedIn:
            customBody = body
            respond = await self.__Request("POST", f"{self.baseUrl}{self.apiPath}{url}")
            if type(respond) != Exception:
                if respond.status_code == 200:
                    return respond.json()
                else:
                    return respond.status_code

    # client name url formatter
    def cleanClientName(self, ganertage):
        return quote(ganertage.encode("utf-8"))

    # helper
    def helper(self, platform, gamertag):
        lookUpType = "id" if platform == platforms.Uno else "gamer"
        if platform not in [platforms.Activision, platforms.Battlenet, platforms.Uno, platforms.All, platforms.PSN,
                            platforms.XBOX]:
            raise InvalidPlatform(platform)
        else:
            if platform in [platforms.Activision, platforms.Battlenet, platforms.Uno]:
                gamertag = self.cleanClientName(gamertag)
        return lookUpType, gamertag

    # API Requests
    async def fullDataReq(self, game, platform, gamertag, type):
        lookUpType, gamertag = self.helper(platform, gamertag)
        return await self.sendRequest(self.fullDataUrl % (game, platform.value, lookUpType, gamertag, type))

    async def combatHistoryReq(self, game, platform, gamertag, type, start, end):
        lookUpType, gamertag = self.helper(platform, gamertag)
        return await self.sendRequest(
            self.combatHistoryUrl % (game, platform.value, lookUpType, gamertag, type, start, end))

    async def breakdownReq(self, game, platform, gamertag, type, start, end):
        lookUpType, gamertag = self.helper(platform, gamertag)
        return await self.sendRequest(
            self.breakdownUrl % (game, platform.value, lookUpType, gamertag, type, start, end))

    async def seasonLootReq(self, game, platform, gamertag):
        lookUpType, gamertag = self.helper(platform, gamertag)
        return await self.sendRequest(self.seasonLootUrl % (game, platform.value, lookUpType, gamertag))

    async def mapListReq(self, game, platform):
        return await self.sendRequest(self.mapListUrl % (game, platform.value))

    async def matchInforReq(self, game, platform, type, matchId):
        return await self.sendRequest(self.matchInfoUrl % (game, platform.value, type, matchId))


# WZ
class WZ(__main__):
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
        data = await self.fullDataReq("mw", platform,  gamertag, "wz")
        return data

    async def combatHistory(self, platform: platforms, gamertag: str, verbose:bool=False, mapping:bool=False):
        data = await self.combatHistoryReq("mw", platform, gamertag, "wz", 0, 0)
        return data

    async def combatHistoryWithDate(self, platform, gamertag: str, start:int, end:int):
        data = await self.combatHistoryReq("mw", platform, gamertag, "wz", start, end)
        return data

    async def breakdown(self, platform, gamertag: str):
        data = await self.breakdownReq("mw", platform, gamertag, "wz", 0, 0)
        return data

    async def breakdownWithDate(self, platform, gamertag: str, start:int, end:int):
        data = await self.breakdownReq("mw", platform, gamertag, "wz", start, end)
        return data

    async def matchInfo(self, platform, matchId:int):
        data = await self.matchInforReq("mw", platform, "wz", matchId)
        return data


# MW
class MW(__main__):
    async def fullData(self, platform, gamertag: str):
        data = await self.fullDataReq("mw", platform, gamertag, "mp")
        return data

    async def combatHistory(self, platform, gamertag: str):
        data = await self.combatHistoryReq("mw", platform, gamertag, "mp", 0, 0)
        return data

    async def combatHistoryWithDate(self, platform, gamertag: str, start: int, end: int):
        data = await self.combatHistoryReq("mw", platform, gamertag, "mp", start, end)
        return data

    async def breakdown(self, platform, gamertag: str):
        data = await self.breakdownReq("mw", platform, gamertag, "mp", 0, 0)
        return data

    async def breakdownWithDate(self, platform, gamertag: str, start: int, end: int):
        data = await self.breakdownReq("mw", platform, gamertag, "mp", start, end)
        return data

    async def seasonLoot(self, platform, gamertag):
        data = await self.seasonLootReq("mw", platform, gamertag)
        return data

    async def mapList(self, platform):
        data = await self.mapListReq("mw", platform)
        return data

    async def matchInfo(self, platform, matchId: int):
        data = await self.matchInforReq("mw", platform, "mp", matchId)
        return data


# CW
class CW(__main__):
    async def fullData(self, platform, gamertag: str):
        data = await self.fullDataReq("cw", platform, gamertag, "mp")
        return data

    async def combatHistory(self, platform, gamertag: str):
        data = await self.combatHistoryReq("cw", platform, gamertag, "mp", 0, 0)
        return data

    async def combatHistoryWithDate(self, platform, gamertag: str, start: int, end: int):
        data = await self.combatHistoryReq("cw", platform, gamertag, "mp", start, end)
        return data

    async def breakdown(self, platform, gamertag: str):
        data = await self.breakdownReq("cw", platform, gamertag, "mp", 0, 0)
        return data

    async def breakdownWithDate(self, platform, gamertag: str, start: int, end: int):
        data = await self.breakdownReq("cw", platform, gamertag, "mp", start, end)
        return data

    async def seasonLoot(self, platform, gamertag):
        data = await self.seasonLootReq("cw", platform, gamertag)
        return data

    async def mapList(self, platform):
        data = await self.mapListReq("cw", platform)
        return data

    async def matchInfo(self, platform, matchId: int):
        data = await self.matchInforReq("cw", platform, "mp", matchId)
        return data


# VG
class VG(__main__):
    async def fullData(self, platform, gamertag: str):
        data = await self.fullDataReq("vg", platform, gamertag, "mp")
        return data

    async def combatHistory(self, platform, gamertag: str):
        data = await self.combatHistoryReq("vg", platform, gamertag, "mp", 0, 0)
        return data

    async def combatHistoryWithDate(self, platform, gamertag: str, start: int, end: int):
        data = await self.combatHistoryReq("vg", platform, gamertag, "mp", start, end)
        return data

    async def breakdown(self, platform, gamertag: str):
        data = await self.breakdownReq("vg", platform, gamertag, "mp", 0, 0)
        return data

    async def breakdownWithDate(self, platform, gamertag: str, start: int, end: int):
        data = await self.breakdownReq("vg", platform, gamertag, "mp", start, end)
        return data

    async def seasonLoot(self, platform, gamertag):
        data = await self.seasonLootReq("vg", platform, gamertag)
        return data

    async def mapList(self, platform):
        data = await self.mapListReq("vg", platform)
        return data

    async def matchInfo(self, platform, matchId: int):
        data = await self.matchInforReq("vg", platform, "mp", matchId)
        return data


# SHOP
class SHOP(__main__):
    async def purchasableItems(self, game: str):
        data = await self.sendRequest(f"/inventory/v1/title/{game}/platform/psn/purchasable/public/en")
        return data

    async def bundleInformation(self, game: str, bundleId):
        data = await self.sendRequest(f"/inventory/v1/title/{game}/bundle/${bundleId}/en")

    async def battlePassLoot(self, platform, season:int):
        data = await self.sendRequest(f"/loot/title/mw/platform/{platform.value}/list/loot_season_{season}/en")
        return data


# USER
class USER(__main__):
    async def friendFeed(self, platform, gamertag:str):
        lookUpType, gamertag = self.helper(platform, gamertag)
        data = await self.sendRequest(f"/userfeed/v1/friendFeed/platform/{platform.value}/gamer/{gamertag}/friendFeedEvents/en")
        return data

    async def eventFeed(self):
        data = await self.sendRequest(f"/userfeed/v1/friendFeed/rendered/en/{self.baseSsoToken}")
        return data

    async def loggedInIdentities(self):
        data = await self.sendRequest(f"/crm/cod/v2/identities/{self.baseSsoToken}")
        return data

    async def codPoints(self, platform, gamertag:str):
        lookUpType, gamertag = self.helper(platform, gamertag)
        data = await self.sendRequest(f"/inventory/v1/title/mw/platform/{platform.value}/gamer/{gamertag}/currency")
        return data

    async def connectedAccounts(self, platform, gamertag:str):
        lookUpType, gamertag = self.helper(platform, gamertag)
        data = await self.sendRequest(f"/crm/cod/v2/accounts/platform/{platform.value}/{lookUpType}/{gamertag}")
        return data

    async def settings(self, platform, gamertag:str):
        lookUpType, gamertag = self.helper(platform, gamertag)
        data = await self.sendRequest(f"/preferences/v1/platform/{platform.value}/gamer/{gamertag}/list")
        return data


# ALT
class ALT(__main__):
    async def search(self, platform, gamertag:str):
        lookUpType, gamertag = self.helper(platform, gamertag)
        data = await self.sendRequest(f"/crm/cod/v2/platform/{platform.value}/username/{gamertag}/search")
        return data


class API(__main__):
    def __init__(self):
        super(API, self).__init__()
        self.Warzone = WZ()
        self.ModernWarfare = MW()
        self.ColdWar = CW()
        self.Vanguard = VG()
        self.Shop = SHOP()
        self.Me = USER()
        self.Misc = ALT()

    # Login
    def login(self, ssoToken: str):
        self.baseHeaders["__X-XSRF-TOKEN"] = self.fakeXSRF
        self.baseHeaders["__X-CSRF-TOKEN"] = self.fakeXSRF
        self.baseHeaders["Atvi-Auth"] = ssoToken
        self.baseHeaders["ACT_SSO_COOKIE"] = ssoToken
        self.baseHeaders["atkn"] = ssoToken
        self.baseHeaders[
            "cookie"] = f'{self.baseCookie}ACT_SSO_COOKIE={ssoToken};XSRF-TOKEN={self.fakeXSRF};API_CSRF_TOKEN={self.fakeXSRF};ACT_SSO_EVENT="LOGIN_SUCCESS:1644346543228";ACT_SSO_COOKIE_EXPIRY=1645556143194;comid=cod;ssoDevId=63025d09c69f47dfa2b8d5520b5b73e4;tfa_enrollment_seen=true;gtm.custom.bot.flag=human;'
        self.baseSsoToken = ssoToken
        self.basePostHeaders["__X-XSRF-TOKEN"] = self.fakeXSRF
        self.basePostHeaders["__X-CSRF-TOKEN"] = self.fakeXSRF
        self.basePostHeaders["Atvi-Auth"] = ssoToken
        self.basePostHeaders["ACT_SSO_COOKIE"] = ssoToken
        self.basePostHeaders["atkn"] = ssoToken
        self.basePostHeaders[
            "cookie"] = f'{self.baseCookie}ACT_SSO_COOKIE={ssoToken};XSRF-TOKEN={self.fakeXSRF};API_CSRF_TOKEN={self.fakeXSRF};ACT_SSO_EVENT="LOGIN_SUCCESS:1644346543228";ACT_SSO_COOKIE_EXPIRY=1645556143194;comid=cod;ssoDevId=63025d09c69f47dfa2b8d5520b5b73e4;tfa_enrollment_seen=true;gtm.custom.bot.flag=human;'
        self.loggedIn = True

        for sub in [self.Warzone, self.ModernWarfare, self.ColdWar, self.Vanguard, self.Shop, self.Me, self.Misc]:
            sub.loggedIn = self.loggedIn
            sub.baseSsoToken = self.baseSsoToken
            sub.baseHeaders = self.baseHeaders
            sub.basePostHeaders = self.basePostHeaders


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
