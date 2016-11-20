# calendar42-API-Proxy
A simple API Proxy package written in Python that combines and caches multiple calls to the Calendar42 Demo API into one single call with a lightweight response in json format.

## Getting started: Setting up the Proxy server
In the command line, we can simply type the following to initialize the Proxy:
```bash
python proxy.py -p $PORT_NUMBER -a $AUTHENTICATION_TOKEN
```
We can pass two optional parameters: the _port number_ and the _authentication token_.
These are set to default as:
```bash
PORT_NUMBER = 8080 
AUTHENTICATION_TOKEN = '43ce3623f44c6bf9ff9a07622eb295ec0d7d2d0a'
# (That is, the TOKEN provided for the assignement)
```

Or in a Python script:
```python
import proxy

proxy.start_proxy()

# If we want to set the parameters:
# proxy.start_proxy(port_number=SOME_PORT_NUMBER, token=SOME_AUTHENTICATION_TOKEN)
```
Again, we can pass the optional arguments _port_number_ and _token_ if we want to.

## Making a GET request to the Proxy server
Making GET requests to the Proxy server is straightforward. It supports the /events-with-subscriptions/$EVENT_ID path format 
(Make sure to request to the same port the Proxy server has been intialized at!).

Using [curl](https://curl.haxx.se/) in the command line:
```bash
curl --request GET http://localhost:8080/events-with-subscriptions/$EVENT-ID/ | python -m json.tool
```
Where EVENT_ID is, of course, the id of your desired event. The `python -m json.tool` command "pretty prints" the json output.

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

## About my design choices
