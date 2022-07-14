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

        self.endPoints = None

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
        print("ssss")
        self.endPoints = endPoints()
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
        return await self.sendRequest(self.endPoints.fullDataUrl % (game, platform, lookUpType, gamertag, type))

    async def combatHistoryReq(self, game, platform, gamertag, type, start, end):
        lookUpType, gamertag = self.helper(platform, gamertag)
        return await self.sendRequest(self.endPoints.combatHistoryUrl % (game, platform, lookUpType, gamertag, type, start, end))

    async def breakdownReq(self, game, platform, gamertag, type, start, end):
        lookUpType, gamertag = self.helper(platform, gamertag)
        return await self.sendRequest(self.endPoints.breakdownUrl % (game, platform, lookUpType, gamertag, type, start, end))

    async def matchInforReq(self, game, platform, type, matchId):
        return await self.sendRequest(self.endPoints.matchInfoUrl % (game, platform, type, matchId))


# WZ
class WZ(API):
    async def fullData(self, platform, gamertag: str):
        data = await self.fullDataReq("mw", platform,  gamertag, "wz")

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


# endPoints
class endPoints:
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


# MW
class MW(API):
    ...


# CW
class CW(API):
    ...


# VG
class VG(API):
    ...


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
