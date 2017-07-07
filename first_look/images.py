# -*-  coding: utf-8 -*-
import json
import falcon

class Resource(object):

    def on_get(self, req, resp): # Bu methodlara responder deniliyormuş
        doc = { 'images':[{'href':'/images/somethings'}] }
        # Json representation of the resource
        resp.body = json.dumps(doc, ensure_ascii=False)
        resp.status = falcon.HTTP_200