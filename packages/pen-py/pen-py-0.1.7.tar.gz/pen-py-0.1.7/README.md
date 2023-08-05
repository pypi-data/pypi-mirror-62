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

**Sign** : A Verifyer and Signer for flask requests using PRIVATE-PUBLIC keys and JWT

**Store** : A light version of ORM using Google Cloud Datastore:
* class Store()
WARNING : to use the datastore, please make sure you reference your google cloud credentials json:

```python
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'pnbx-rd-xxxxxxxx.json'
```

- [ ] Please request the json file of r&d account for testing
    
