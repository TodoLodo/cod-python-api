# cod-python-api
**Call Of Duty API Library** for **python** with the implementation of both public and private API used by activision on 
callofduty.com
<br>
<br>
## Devs
[Todo Lodo](https://github.com/TodoLodo2089) and [Engineer15](https://github.com/Engineer152)
<br>
<br>
## Documentation
This package can be used directly as a python file or as a python library
### Installation
 For direct use 
 <br>
```
git clone https://github.com/TodoLodo2089/cod-python-api.git
```
<br>
As a python library

```
pip install git+https://github.com/TodoLodo2089/cod-python-api.git
```
<br>

### Usage
#### Initiation
Import module with its classes
<br>
```
from cod_api import API, platforms, games, friendActions

api = API()
```
<br>
Login with your sso token

```
api.login('Your sso token')
```
You sso token can be found by longing in at [callofduty](https://my.callofduty.com/), opening dev tools (ctr+shift+I),
going to Applications > Storage > Cookies > <span>https</span>://callofduty.com, filter to search 'ACT_SSO_COOKIE' and 
copy the value
<br><br>
#### Retrieving game profile
A player's game profile can be retrieved by using API sub game classes with its function fullData(platform, gamertag)

*Example*
```
profileData = api.ModernWarfare.fullData(platforms.Battlenet, "Username#1234")
```
*Output* > json
<br><br>
#### Retrieving combat history
A player's game profile can be retrieved by using API sub game classes with its functions combatHistory(platform, gamertag) or 
combatHistoryWithDate(platform, gamertag, start, end)

*Example*
```
matchHistory = api.Warzone.combatHistory(platforms.Activision, "Username#123456")
```
*Output* > json