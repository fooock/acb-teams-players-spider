#!/usr/bin/env python
# -*- coding: utf-8 -*-

import aerospike

class AerospikeConnector(object):

    def __init__(self, bootstrap_server, bootstrap_port):
        self.config = {'hosts': [(bootstrap_server, bootstrap_port)]}
        self.client = None

    def open_connection(self):
        if self.client is None:
            try:
                self.client = aerospike.client(self.config).connect()
            except Exception as e:
                import sys
                print("error: {0}".format(e), file=sys.stderr)
                sys.exit(1)

    def close_connection(self):
        if self.client is not None:
            self.client.close()

    def get_and_close(self, key, as_namespace, as_set):
        """The connection is automatically closed after the call"""
        try:
            value = self.get(key, as_namespace, as_set)
            self.close_connection()
            return value
        except:
            return None

    def exists(self, key, as_namespace, as_set):
        """Check a record. The connection is created (if it is not already) and
        it keeps opened until it is manually closed.
        """
        self.open_connection()
        _, meta = self.client.exists((as_namespace, as_set, key))
        if meta is None:
            return False
        else:
            return True

    def get(self, key, as_namespace, as_set):
        """Get a record. The connection is created (if it is not already) and
        it keeps opened until it is manually closed.
        """
        self.open_connection()
        try:
            (as_key, metadata, record) = \
                self.client.get((as_namespace, as_set, key))
            return record['value']
        except:
            return None

    def put(self, key, value, as_namespace, as_set):
        """Put a record. The connection is created (if it is not already) and
        it keeps opened until it is manually closed.
        """
        self.open_connection()
        as_key = (as_namespace, as_set, key)
        self.client.put(as_key, {
            'key': key,
            'value': value
        })


connector = AerospikeConnector('localhost', 3000)

import json
import unidecode

with open('players.json') as data_file:
    data = json.load(data_file)

    for i, item in enumerate(data):
        entity_id = f'P{i}'
        print(entity_id)

        names = []

        name = unidecode.unidecode(' '.join(item['player_name'].strip().split())).lower()
        names.append(name)
        name = name.replace('.', '')
        names.append(name)
        name_parts = name.split(" ")
        # Name with a single second/last name
        name_len = len(name_parts)
        if name_len > 2:
            name = name_parts[0] + " " + name_parts[1]
            names.append(name)
            name_parts = name.split('-')
            name_len = len(name_parts)
            if name_len > 2:
                name = name_parts[0] + " " + name_parts[1]
                names.append(name)
        if "'" in name:
            name = name.replace("'", '')
            names.append(name)

        if 'twitter' in item:
            nickname = item['twitter'].strip()[1:]
            names.append(nickname)

        for name in names:
            connector.put(name, entity_id, 'polypus_twttr', 'entities')

with open('teams.json') as data_file:
    data = json.load(data_file)
    for i, item in enumerate(data):
        entity_id = f'T{i}'
        print(entity_id)

        names = []

        name = unidecode.unidecode(' '.join(item['name'].strip().split())).lower()

        # Special case
        if 'murcia' in name:
            names.append(name)
            names.append('ucam murcia')
        elif 'barcelona' in name:
            names.append(name)
            names.append('fcb basket')
        elif 'madrid' in name:
            names.append('real madrid basket')
            names.append('real madrid baloncesto')
        else:
            names.append(name)

        name = name.replace('.', '')
        names.append(name)
        name_parts = name.split(" ")
        # Name with a single second/last name
        name_len = len(name_parts)
        if name_len > 2:
            name = name_parts[0] + " " + name_parts[1]
            names.append(name)
            name_parts = name.split('-')
            name_len = len(name_parts)
            if name_len > 2:
                name = name_parts[0] + " " + name_parts[1]
                names.append(name)
        if "'" in name:
            name = name.replace("'", '')
            names.append(name)

        if 'twitter' in item:
            nickname = item['twitter'].strip()[1:]
            names.append(nickname)

        for name in names:
            connector.put(name, entity_id, 'polypus_twttr', 'entities')
