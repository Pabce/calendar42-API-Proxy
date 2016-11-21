# calendar42-API-Proxy
A simple API Proxy package written in Python 3. It combines and caches multiple calls to the Calendar42 Demo API into one single call with a lightweight response (which will be in json format).

## Getting started: Setting up the Proxy server
In the command line, we can simply type the following to initialize the Proxy:
```bash
python proxy.py
```
We can pass two optional parameters: the _port number_ and the _authentication token_:
```bash
python proxy.py -p $PORT_NUMBER -a $AUTHENTICATION_TOKEN
```
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
Again, we can pass the optional parameters _port_number_ and _token_ if we want to.

## Making a GET request to the Proxy server
Making GET requests to the Proxy server is straightforward. It supports the /events-with-subscriptions/$EVENT_ID/ path format 
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
_First of all, I'm writing this when I'm not far from completing the assignment, rather than at the beginning like requested. The reason for this is simply because I was unsure about how to complete it before I started, as I have only some experience with HTTP and the Django library (which I initially thought I would need to use).  
Therefore, I thought it made no sense to write an inaccurate and prone to change 'guideline', and it would be much more efficient to write it all at once at the end._

#### Library choices
As I got into the assignement, I realized it was probably simple enough to be done with the standard python library, without need to use third party libraries such as [Django](https://www.djangoproject.com/).

Therefore, mi initial choices for making requests to the C42 API and setting up the Proxy server where [urllib](https://docs.python.org/3/library/urllib.html) and [http.server](https://docs.python.org/3/library/http.server.html).

Further into coding, however, I decided to switch to the [requests](http://docs.python-requests.org/en/master/) library, which I found to be a powerful and very efficient tool for sending HTTP requests.

Finally, I used the [pyTest](http://doc.pytest.org/) library for unit testing. The tests can be found in the unit_test folder an can be run with the following command:
```bash
py.test -v unit_test.py
```

#### Project structure
The project consists of the following files:
* [proxy.py](https://github.com/Pabce/calendar42-API-Proxy/blob/master/proxy.py) contains the Handler class, which manages all the requests passed on to the Proxy. When the Handler receives a request, it will check if it has the expected format, and return an error to the client if it does not. If it does, it will send the required GET requests through the GetRequest class in request_to_C42.py and return the requested data (or return the data directly from the cache). 

* [request_to_C42.py](https://github.com/Pabce/calendar42-API-Proxy/blob/master/request_to_C42.py) contains the GetRequest class. Each instance of this class is used to send one or more GET requests to the C42 API, and filter and merge them into the requested format. This class can be modified and extended in the future to be able to send any kind of requests to the C42 API, and merge the response in any way we like.

* [cache_manager.py](https://github.com/Pabce/calendar42-API-Proxy/blob/master/cache_manager.py) contains the CacheManager class. This class is the one in charge (as the name suggests) of managing the proxy cache. It stores the cached values for each distinct EVENT_ID that the client has requested, and also the time at when they were cached. It contains methods used by the Handler class to determine wheter the cached value should be returned to the client or rather a new request to the C42 API should be sent. 

I also added an `__init__.py` module so the modules could be imported directly with their names.

The proxy itself is initialized by running the proxy.py module, as explained above.

#### Bottom line
Despite not having much time I enjoyed doing the assignment very much, it refreshed my memory on a few things I had forgotten and I also learned some new skills!

I'm really excited about the possibility of working at C42, and even if this doesn't make the cut I'm happy to have learned new stuff and become a bit better at one of the things I'm passionate about.
