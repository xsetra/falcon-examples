# -*- coding: utf-8 -*-

import falcon
import json

from .db_client import RethinkClient


class NoteResource:

    def __init__(self, db_client):
        """ Note resource for falcon
        :param db_client: RethinkClient object for database resource
        """
        self.__db_client = db_client

    def on_get(self, req, resp):
        """ Handles GET Requests. Fetch one or all todo notes
        :param req:
        :param resp:
        :return: Note for particular ID
        """
        if req.get_param('id'):
            result = self.__db_client.get_note(req.get_param('id'))
        else:
            result = self.__db_client.get_notes()
        resp.body = json.dumps(result)

    def on_post(self, req, resp):
        """ Handles POST Requests. Add a new todo note.
        :param req:
        :param resp:
        :return: Status
        """
        try:
            raw_json = req.stream.read()
        except Exception as ex:
            raise falcon.HTTPError(falcon.HTTP_400, 'Error', ex.message)

        try:
            req_json = json.loads(raw_json)
            sid = self.__db_client.add_note(id=req_json['id'], title=req_json['title'], content=req_json['content'])
            resp.body = 'Successfully inserted, sid={}'.format(sid)
        except ValueError:
            raise falcon.HTTPError(falcon.HTTP_400, 'Invalid JSON', 'The JSON was incorrect')


db_client = RethinkClient(host='localhost', port=28015, db='todo')
db_client.db_setup()
db_client.table_setup(table_name='notes')

api = application = falcon.API()
api.add_route('/notes', NoteResource(db_client))
