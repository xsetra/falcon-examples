# -*- coding: utf-8 -*-

import os
import rethinkdb
from rethinkdb.errors import RqlDriverError, RqlRuntimeError


class RethinkClient:

    def __init__(self, host, port, db):
        """ Create rethinkdb client.
        :param host: hostname, i.e : localhost
        :param port: port, i.e : 28015
        :param db: database name : i.e : testdb
        """
        self.__host = host
        self.__port = port
        self.__db = db

    def db_setup(self):
        try:
            rethinkdb.db_create(self.__db).run(self.__db_connection)
            print('{} database setup completed'.format(self.__db))
        except RqlRuntimeError:
            print('{} database exist. Going on.'.format(self.__db))

    def connect(self):
        try:
            self.__db_connection = rethinkdb.connect(host=self.__host, port=self.__port)
        except:
            raise RuntimeError('Database connection error!')

    def table_setup(self, table_name):
        try:
            rethinkdb.db(self.__db).table_create(table_name).run(self.__db_connection)
            print('{} table creation completed.'.format(table_name))
        except RqlRuntimeError:
            print('Table already exists. Nothing to do.')

    def get_note(self, note_id):
        """ Fetch a note from database by particular ID.
        :param note_id: note id
        :return: Fetched note type:<dict>
        """
        note = rethinkdb.db(self.__db).table('notes').get(note_id).run(self.__db_connection)
        result = {'note':note}
        return result

    def get_notes(self):
        """ Fetch all notes from database
        :return: Fetched notes type:<dict>
        """
        cursor = rethinkdb.db(self.__db).table('notes').run(self.__db_connection)
        result = {'notes':[n for n in cursor]}
        return result