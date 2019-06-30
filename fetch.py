#!/usr/bin/env python3

import getopt
import json
import sqlite3
import sys
import time

import requests

opts, _ = getopt.getopt(sys.argv[1:], "t:c:d:")
opts = dict(opts)
token = opts['-t']
chan_id = opts['-c']
db_path = opts['-d']
before = None
conn = sqlite3.connect(db_path)

try:
    while True:
        uri = 'https://discordapp.com/api/channels/' + chan_id + '/messages?token=' + token + '&limit=100' + ('&before=' + before if before else '')
        print(uri)
        response = requests.get(uri)
        messages = json.loads(response.content.decode('utf-8'))

        if not messages:
            break

        if response.status_code == 429:
            print('Should retry after ' + response.headers['Retry-After'] + ' seconds.')

        for msg in messages:
            user = msg['author']['username'] + '#' + msg['author']['discriminator']
            conn.execute('INSERT INTO raw_message VALUES (?,?,?,?)', (msg['id'], msg['timestamp'], user, msg['content']))

        before = messages[len(messages) - 1]['id']
        time.sleep(0.1)
finally:
    conn.commit()
