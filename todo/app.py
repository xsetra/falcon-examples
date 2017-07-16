# -*- coding: utf-8 -*-

import falcon
import json

from wsgiref import simple_server
from db_client import RethinkClient


class NoteResource(object):

    def __init__(self, db_client):
        """ Note resource for falcon
        :param db_client: RethinkClient object for database resource
        """
        self.__db_client = db_client

    def on_get(self, req, resp):
        """ Handles GET Requests. Fetch one or all todo notes
        :param req:
        :param resp:
        :return:
        """
        if 'id' in req.context['body']:
            if req.context['body']['id'] != -1:
                req.context['result'] = self.__db_client.get_note(req.context['body']['id'])
            else:
                req.context['result'] = self.__db_client.get_notes()
        else:
            req.context['result']=falcon.HTTPBadRequest(title='You must send a particular note id or -1')


    def on_post(self, req, resp):
        """ Handles POST Requests. Add a new todo note.
        :param req:
        :param resp:
        :return:
        """
        sid = self.__db_client.add_note(id=req.context['body']['id'],
                                                          title=req.context['body']['title'],
                                                          content=req.context['body']['content'])
        if sid['inserted'] == 1:
            # Insertion succeded.
            req.context['result'] = {'result':'Note added successfully.'}
        else:
            req.context['result'] = {'result':'Note was not added'}


    def on_delete(self, req, resp):
        """ Delete a note from database.
        :param req:
        :param resp:
        :return: Succcess id.
        """
        pass

class JsonMiddleware(object):

    def process_request(self, req, resp):
        """ Process request before to routing responder method. Is JSON correct?
        :param req:
        :param resp:
        :return:
        """
        if not req.client_accepts_json:
            # If client doesn't support JSON
            raise falcon.HTTPNotAcceptable('This API only supports encoded as JSON')

        if 'application/json' not in req.content_type:
            # If content type of header is not application/json
            raise falcon.HTTPUnsupportedMediaType('This API only supports requests encoded as JSON')


class JsonTranslatorMiddleware(object):

    def process_request(self, req, resp):
        """ Process request. Decode request
        :param req:
        :param resp:
        :return:
        """
        body = req.stream.read()
        if not body:
            raise falcon.HTTPBadRequest(title='Empty request body',
                                        description='A valid JSON is required')
        try:
            req.context['body'] = json.loads(body.decode('utf8'))

        except (ValueError, UnicodeDecodeError):
            raise falcon.HTTPError(status=falcon.HTTP_753,
                                   title='Malformed JSON',
                                   description='Could not decode the request body. The JSON was incorrect or not encoded as UTF-8')

    def process_response(self, req, resp, resource):
        """ Process response before the response wasn't send to client
        :param req:
        :param resp:
        :param resource:
        :return:
        """
        if 'result' not in req.context:
            return

        resp.body = json.dumps(req.context['result'])




db_client = RethinkClient(host='localhost', port=28015, db='todo')
db_client.db_setup()
db_client.table_setup(table_name='notes')

api = application = falcon.API(middleware=[JsonMiddleware(),
                                           JsonTranslatorMiddleware()])
api.add_route('/notes', NoteResource(db_client))

if __name__ == '__main__':
    httpd = simple_server.make_server('127.0.0.1', 8001, api)
    httpd.serve_forever()