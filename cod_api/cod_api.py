# Imports
import enum
import requests
from urllib.parse import quote
import uuid


class API:
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
        self.fakeXSRF = uuid.uuid4()
        self.userAgent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
        self.baseCookie: str = "new_SiteId=cod;ACT_SSO_LOCALE=en_US;country=US;"
        self.baseSsoToken: str
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

        # Class Variables
        self.Warzone = self.ModernWarfare = self.ColdWar = self.Vanguard = self.Shop = self.Me = self.Misc = None

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
            return requests.request(method=method, url=url, headers=h, data=b)
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

    # Login
    def login(self, ssoToken: str):
        self.Warzone = WZ()
        self.ModernWarfare = MW()
        self.ColdWar = CW()
        self.Vanguard = VG()
        self.Shop = SHOP()
        self.Me = USER()
        self.Misc = ALT()
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

    # client name url formatter
    def cleanClientName(self, ganertage):
        return quote(ganertage.encode("utf-8"))

    # helper
    def helper(self, platform, gamertag):
        lookUpType = "id" if platform == platforms.Uno else "gamer"
        if platform not in [platforms.Activision, platforms.Battlenet, platforms.Uno, platforms.All, platforms.PSN, platforms.XBOX]:
            raise InvalidPlatform(platform)
        else:
            if platform in [platforms.Activision, platforms.Battlenet, platforms.Uno]:
                gamertag = self.cleanClientName(gamertag)
        return lookUpType, gamertag

    # API Requests
    async def fullDataReq(self, game, platform, gamertag, type):
        lookUpType, gamertag = self.helper(platform, gamertag)
        print(self.fullDataUrl % (game, platform.name, lookUpType, gamertag, type))
        return await self.sendRequest(self.fullDataUrl % (game, platform.name, lookUpType, gamertag, type))

    async def combatHistoryReq(self, game, platform, gamertag, type, start, end):
        lookUpType, gamertag = self.helper(platform, gamertag)
        return await self.sendRequest(self.combatHistoryUrl % (game, platform.name, lookUpType, gamertag, type, start, end))

    async def breakdownReq(self, game, platform, gamertag, type, start, end):
        lookUpType, gamertag = self.helper(platform, gamertag)
        return await self.sendRequest(self.breakdownUrl % (game, platform.name, lookUpType, gamertag, type, start, end))

    async def seasonLootReq(self, game, platform, gamertag):
        lookUpType, gamertag = self.helper(platform, gamertag)
        return await self.sendRequest(self.seasonLootUrl % (game, platform.name, lookupType, gamertag))

    async def mapListReq(self, game, platform):
        return await self.sendRequest(self.endPoints.mapListUrl % (game, platform.name))

    async def matchInforReq(self, game, platform, type, matchId):
        return await self.sendRequest(self.matchInfoUrl % (game, platform.name, type, matchId))


# WZ
class WZ(API):
    async def fullData(self, platform, gamertag: str):
        data = await self.fullDataReq("mw", platform,  gamertag, "wz")
        return data

    async def combatHistory(self, platform, gamertag: str):
        data = await self.combatHistoryReq("mw", platform, gamertag, "wz", 0, 0)

    async def combatHistoryWithDate(self, platform, gamertag: str, start:int, end:int):
        data = await self.combatHistoryReq("mw", platform, gamertag, "wz", start, end)

    async def breakdown(self, platform, gamertag: str):
        data = await self.breakdownReq("mw", platform, gamertag, "wz", 0, 0)

    async def breakdownWithDate(self, platform, gamertag: str, start:int, end:int):
        data = await self.breakdownReq("mw", platform, gamertag, "wz", start, end)

    async def matchInfo(self, platform, matchId:int):
        data = await self.matchInforReq("mw", platform, "wz", matchId)


# MW
class MW(API):
    async def fullData(self, platform, gamertag: str):
        data = await self.fullDataReq("mw", platform, gamertag, "mp")

    async def combatHistory(self, platform, gamertag: str):
        data = await self.combatHistoryReq("mw", platform, gamertag, "mp", 0, 0)

    async def combatHistoryWithDate(self, platform, gamertag: str, start: int, end: int):
        data = await self.combatHistoryReq("mw", platform, gamertag, "mp", start, end)

    async def breakdown(self, platform, gamertag: str):
        data = await self.breakdownReq("mw", platform, gamertag, "mp", 0, 0)

    async def breakdownWithDate(self, platform, gamertag: str, start: int, end: int):
        data = await self.breakdownReq("mw", platform, gamertag, "mp", start, end)

    async def seasonLoot(self, platform, gamertag):
        data = await self.seasonLootReq("mw", platform, gamertag)

    async def mapList(self, platform):
        data = await self.mapListReq("mw", platform)

    async def matchInfo(self, platform, matchId: int):
        data = await self.matchInforReq("mw", platform, "mp", matchId)


# CW
class CW(API):
    async def fullData(self, platform, gamertag: str):
        data = await self.fullDataReq("cw", platform, gamertag, "mp")

    async def combatHistory(self, platform, gamertag: str):
        data = await self.combatHistoryReq("cw", platform, gamertag, "mp", 0, 0)

    async def combatHistoryWithDate(self, platform, gamertag: str, start: int, end: int):
        data = await self.combatHistoryReq("cw", platform, gamertag, "mp", start, end)

    async def breakdown(self, platform, gamertag: str):
        data = await self.breakdownReq("cw", platform, gamertag, "mp", 0, 0)

    async def breakdownWithDate(self, platform, gamertag: str, start: int, end: int):
        data = await self.breakdownReq("cw", platform, gamertag, "mp", start, end)

    async def seasonLoot(self, platform, gamertag):
        data = await self.seasonLootReq("cw", platform, gamertag)

    async def mapList(self, platform):
        data = await self.mapListReq("cw", platform)

    async def matchInfo(self, platform, matchId: int):
        data = await self.matchInforReq("cw", platform, "mp", matchId)


# VG
class VG(API):
    async def fullData(self, platform, gamertag: str):
        data = await self.fullDataReq("vg", platform, gamertag, "mp")

    async def combatHistory(self, platform, gamertag: str):
        data = await self.combatHistoryReq("vg", platform, gamertag, "mp", 0, 0)

    async def combatHistoryWithDate(self, platform, gamertag: str, start: int, end: int):
        data = await self.combatHistoryReq("vg", platform, gamertag, "mp", start, end)

    async def breakdown(self, platform, gamertag: str):
        data = await self.breakdownReq("vg", platform, gamertag, "mp", 0, 0)

    async def breakdownWithDate(self, platform, gamertag: str, start: int, end: int):
        data = await self.breakdownReq("vg", platform, gamertag, "mp", start, end)

    async def seasonLoot(self, platform, gamertag):
        data = await self.seasonLootReq("vg", platform, gamertag)

    async def mapList(self, platform):
        data = await self.mapListReq("vg", platform)

    async def matchInfo(self, platform, matchId: int):
        data = await self.matchInforReq("vg", platform, "mp", matchId)


# SHOP
class SHOP(API):
    ...


# USER
class USER(API):
    ...


# ALT
class ALT(API):
    ...


# Enums
class platforms(enum.Enum):
    All = 'all'
    Activision = 'uno'
    Battlenet = 'battle'
    PSN = 'psn'
    Steam = 'steam'
    Uno = 'uno'
    XBOX = 'xbl'


class friendActions(enum.Enum):
    Invite = "invite"
    Uninvite = "uninvite"
    Remove = "remove"
    Block = "block"
    Unblock = "unblock"


class InvalidPlatform(Exception):
    def __init__(self, platform: platforms):
        self.message: str
        if platform == platforms.Steam:
            self.message = "Steam Doesn't exist for MW. Try `battle` instead."
        else:
            self.message = f"Invalid platform, use platform class!"

    def __str__(self):
        return self.message
