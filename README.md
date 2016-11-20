# calendar42-API-Proxy
A simple API Proxy package written in Python that combines and caches multiple calls to the Calendar42 Demo API into one single call with a lightweight response.

## Getting started: Setting up the Proxy server.
In the command line, we can simply write the following to initialize the Proxy:
```bash
python proxy.py $OPTIONAL_AUTHENTICATION_TOKEN
```

Or in a Python script:
```python
import proxy

proxy.start_proxy()
```

## Making a GET request to the Proxy server.
Making GET requests to the Proxy server is straightforward. It supports the /events-with-subscriptions/$EVENT_ID path format 
(Make sure to request to the same port the server has been intialized at!).

Using [curl](https://curl.haxx.se/) in the command line:

Or in a Python script, using the [requests](http://docs.python-requests.org/en/master/) library:
```python
import json
import requests

EVENT_ID = '4e662f73d806f4caee212a1656130a73_14770730517003'

r = requests.get("http://localhost:8080/events-with-subscriptions/{}/".format(EVENT_ID))

r_json = r.json()
print(json.dumps(r_json, sort_keys=True, indent=4))
```
The [proxy_request.py](https://github.com/Pabce/calendar42-API-Proxy/blob/master/proxy_request.py) module included in the files does exactly this.

## About my design choices.
