# Penbox Python 

**v0.1.7 available**: 

```console
pip install pen-py
```

```python
from penpy import DicPlus, Store
```
## Included:

**DicPlus** : A advanced Ordered Dictionnary using . for referecing. 
* class DicPlus()
* Includes a following functions:
    * format()
    * mapping()
    * overwrite()
    * clean_json()
    * from_json()
    * pprint()

**Dates** : A light version of dates handling:
* absolute_date() : from ISO-like to datetime
* relative_date() : from timedelta-like string to datetime
* str_to_timedelta() : from timedelta-like string to timedelta

**Secure** : A full version that helps to manage authentication, authorization, signature and signature verification
```python
# app.py create_app()

SECRETS = DicPlus.from_json('secrets.json').secrets 
# Please ask if you need the secrets.json file, that containts auth0 credentials and a PRIVATE-PUBLIC key set for signature.

from .secure import *

mykeyset = KeySet(jsonfile = "keySet.json")

mysecurity = Secure(
    service = "https://notif.pnbx.cc", # Notify here your service
    private_key=SECRETS.private_key,
    authenticator = {
        "client_id":SECRETS.auth0.client_id,
        "client_secret":SECRETS.auth0.client_secret,
        "domain":SECRETS.auth0.domain
    },
    keySet = mykeyset
)

app.secure = mysecurity

```
```python
# anywhere in the code:

# create bearer headers : authenticate to service (token is automatically refreshed if required only):
headers = app.secure.auth_headers()

# create signature headers with signed body included:
headers = app.secure.signed_headers(body, "https://notif.pnbx.cc")

# verify signature against issuers (MUST BE IN KEYSET):
@app.route('/test_signature')
@app.secure.verify(issuers = ["https://notif.pnbx.cc", "https://penbox.eu.auth0.com/"])
def test_signature():

# authorize API calls for a specific scope:
@app.route('/test_authorize')
@app.secure.authorize("sms:send email:send")
def test_authorize():

```

**Store** : A light version of ORM using Google Cloud Datastore:
* class Store()
WARNING : to use the datastore, please make sure you reference your google cloud credentials json:

```python
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'pnbx-rd-xxxxxxxx.json'
```

- [ ] Please request the json file of r&d account for testing
    
