This is the official [python](https://python.org/) client for [Dr. Ashtetepe](https://drhttp.com/) service.


DrHTTP let's you record two types of requests :

 - Inbound : requests that are performed by clients of your server (eg. API calls from a mobile app)
 - Outbound (optional) : requests that are performed by your server (eg. API call to third parties)

Note: You need to configure inbound request recording to have outbound request recording working.

# Installation

 1) Install package with `pip` (or any compatible package manager) :
    ```
    pip install drhttp
    ```

 2) You will need a `dsn` ([Data source name](https://en.wikipedia.org/wiki/Data_source_name)) which can be found in [your project](https://drhttp.com/projects).

# Usage for [Django](https://www.djangoproject.com/)

[An integraion example is provided here](https://bitbucket.org/drhttp/drhttp-python/src/master/examples/django/)

## Inbound request recording


This recording is done via a [wsgi](https://en.wikipedia.org/wiki/Web_Server_Gateway_Interface) middleware. You can configure it in `wsgi.py`:

```python
application = ... # get your application from existing code

import drhttp
application = drhttp.WSGIMiddleware(app=application,
                                    dsn="<insert_dsn_here")
```

### User identification

It allows the identification of the user issuing the inbound request. You'll be able to filter requests based on this field in the web interface. `drhttp` will identify your user if you set the `x-drhttp-user` response header with the user's id as value. Fortunately, we provide you a django middleware that does it automaticaly.

```python
MIDDLEWARE = [
    ...
    'drhttp.DjangoUserMiddleware',
]
```

### Device identification

Device identification works as user identification, only the header name changes (`x-drhttp-device`). No django middleware is provided though, it's up to you to set this header depending your device identification strategy.

## Outbound request recording

*Note: Outbound request recording is not available yet in the python library*

# Usage for [Flask](https://www.djangoproject.com/)

[An integraion example is provided here](https://bitbucket.org/drhttp/drhttp-python/src/master/examples/flask/)

## Inbound request recording

This recording is done via a wsgi middleware. You may need to change some code in your flask app file.
The goal is to encapsulate the wsgi app in the drhttp middleware. As `drhttp.WSGIMiddleware()` returns a wsgi application (not a full flask application) it can't be run by flask cli, you need a wsgi application server like `werkzeug/gunicorn/uwsgi`.

```python
...
app = Flask(__name__)
...

if __name__ == '__main__':
    import drhttp
    from werkzeug.serving import run_simple
    app = drhttp.WSGIMiddleware(app=app, dsn="<insert_dsn_here>")
    run_simple('0.0.0.0', 80, app)
```

### User identification

It allows the identification of the user issuing the inbound request. You'll be able to filter requests based on this field in the web interface. `drhttp` will identify your user if you set the `x-drhttp-user` response header with the user's id as value.

Here is an example if you use `Flask-HTTPAuth` :

```python
from drhttp import DRHTTP_HEADER_USER
@app.after_request
def apply_caching(response):
    response.headers[DRHTTP_HEADER_USER] = auth.username()
    return response
```

### Device identification

Device identification works as user identification, only the header name changes (`x-drhttp-device`). It's up to you to set this header depending your device identification strategy.

## Outbound request recording

*Note: Outbound request recording is not available yet in the python library*

# Troubleshooting

Please [report any issue](https://bitbucket.org/drhttp/drhttp-python/issues/new) you encounter concerning documentation or implementation. This is very much appreciated.