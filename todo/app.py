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
        """ Handles GET Requests
        :param req:
        :param resp:
        :return: Note for particular ID
        """
        if req.get_param('id'):
            result = self.__db_client.get_note(req.get_param('id'))
        else:
            result = self.__db_client.get_notes()
        resp.body = json.dumps(result)

db_client = RethinkClient(host='localhost', port=28015, db='todo')
db_client.table_setup(table_name='notes')

api = application = falcon.API()
api.add_route('/notes', NoteResource(db_client))
