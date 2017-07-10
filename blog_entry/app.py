# -*- coding: utf-8 -*-

import falcon


class BlogEntry(object):
    def __init__(self, db_client):
        self._post_ctrl = db_client

    def on_get(self, request, response, author, post):
        content = self._post_ctrl.get(author, post)
        if not content:
            raise falcon.exceptions.HTTPNotFound()
        response.content_type = "application/json"
        response.body = content['body']
        response.status = falcon.HTTP_200
