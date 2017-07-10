# -*-  coding: utf-8 -*-
import json
import falcon
import msgpack
import io

class Resource(object):

    def on_get(self, req, resp): # Responder with JSON
        doc = {
            'images':[
                {'href2':'/images/somethings'}
            ]
        }
        # Json representation of the resource
        # resp.body = json.dumps(doc, ensure_ascii=False)
        # resp.status = falcon.HTTP_200
        resp.data = msgpack.packb(doc, use_bin_type=True)
        resp.content_type = 'application/msgpack'
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp): # Responder with MSGPACK
        doc = {'images':[ {'href':'/images/something'} ]}
        resp.data = msgpack.packb(doc, use_bin_type=True)
        resp.content_type = 'application/msgpack'
        resp.status = falcon.HTTP_200