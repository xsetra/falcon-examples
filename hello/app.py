# -*- coding: utf-8 -*-

import falcon

class Hello(object):
    def on_get(self, request, response):
        response.body = "Hello"
        response.status = falcon.HTTP_200

    def on_post(self, request, response):
        response.body = "Hello via POST method"
        response.status = falcon.HTTP_200

# application variable name is needed for Gunicorn wsgi web server.
app = application = falcon.API()
app.add_route('/', Hello())

"""
gunicorn hello.app --reload

http POST 127.0.0.1:8000/
curl -X POST 127.0.0.1:8000/

"""