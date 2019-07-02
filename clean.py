#!/usr/bin/env python3

import re
import sys
import sqlite3

user_list = [s.strip() for s in sys.stdin.readlines()]

rLine = re.compile(r'[\r\n]')
rCmd = re.compile(r'[/;&!][0-9a-z]+', re.IGNORECASE)
rUri = re.compile(r'[a-z]+://[^\s]+', re.IGNORECASE)
rRef = re.compile(r'<[@!#]+[0-9]+>')
rHere = re.compile(r'@(everyone|here)')
rMono = re.compile(r'`.*?`')
rSpace = re.compile(r'[ \t]+')

db_path = sys.argv[1]
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
c = conn.execute('SELECT * FROM raw_message t1 WHERE t1.id NOT IN (SELECT t2.id FROM clean_message t2)')

while True:
    row_list = c.fetchmany(100)

    if not row_list:
        break

    for row in row_list:
        row = dict(row)
        # Remove non Latin chars
        row['content'] = row['content'].encode('iso-8859-1', 'ignore').decode('iso-8859-1')

        # Ignore non whitelisted users
        if row['user'] not in user_list:
            continue

        # Ignore multiline messages
        if rLine.search(row['content']) != None:
            continue

        # Ignore command messages
        if rCmd.match(row['content'].strip()) != None:
            continue

        # Remove garbage
        row['content'] = rUri.sub(' ', row['content'])
        row['content'] = rRef.sub(' ', row['content'])
        row['content'] = rHere.sub(' ', row['content'])
        row['content'] = rMono.sub(' ', row['content'])
        row['content'] = rSpace.sub(' ', row['content'])
        row['content'] = row['content'].strip()

        # Ignore empty message
        if not row['content']:
            continue

        # Insert clean line
        conn.execute('INSERT INTO clean_message VALUES (?,?,?,?)', tuple(row.values()))

conn.commit()
