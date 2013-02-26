#!/usr/bin/env python
# coding=utf-8
import os
import sqlite3
import argparse
import time


# How long to wait after Skype loading before patching db
WAIT_AFTER_START = 10

SKYPE_DIR = os.path.join(os.path.expanduser("~"), "Library/Application Support/Skype/")

SKYPE_APP = "/Applications/Skype.app"

SQL_PATCH = """
CREATE TABLE IF NOT EXISTS skypelog (message_id INTEGER, author TEXT, from_dispname TEXT, timestamp INTEGER, old_body_xml TEXT, new_body_xml TEXT);

DROP TRIGGER IF  EXISTS update_skypelog;

CREATE TRIGGER update_skypelog
AFTER UPDATE OF body_xml
ON Messages
FOR EACH ROW
WHEN NEW.body_xml != OLD.body_xml
BEGIN

INSERT INTO skypelog (message_id, author, from_dispname, timestamp, old_body_xml, new_body_xml)
values (new.id, new.author, new.from_dispname, new.timestamp,old.body_xml, new.body_xml);

END;
"""

SQL_GET_EDITED_MESSAGES = "SELECT author, from_dispname, old_body_xml, new_body_xml FROM skypelog ORDER BY timestamp DESC LIMIT 10;"

TEMPLATE_USER = """
======================================
== {user}
======================================"""

TEMPLATE_MESSAGE = """{from_dispname} ({author})
Old message: {old_body_xml}
New message: {new_body_xml}
--------------------------------------"""


def get_skype_users():
    """Get user names of all Skype users installed on this computer"""
    for name in os.listdir(SKYPE_DIR):
        potential_user = os.path.join(SKYPE_DIR, name)
        if os.path.isdir(potential_user) and 'main.db' in os.listdir(potential_user):
            yield name


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Skype launcher and viewer of edited Skype messages.')
    parser.add_argument('--show', action='store_true',
                        help='If this argument is passed, last edited messages will be shown. '
                             'Otherwise Skype will be launched and patched.')
    args = parser.parse_args()

    if args.show:
        for user in get_skype_users():
            conn = sqlite3.connect(os.path.join(SKYPE_DIR, user, 'main.db'))
            c = conn.cursor()
            print TEMPLATE_USER.format(user=user)
            for row in c.execute(SQL_GET_EDITED_MESSAGES):
                print TEMPLATE_MESSAGE.format(
                    author=row[0],
                    from_dispname=row[1].encode('utf-8'),
                    old_body_xml=row[2].encode('utf-8'),
                    new_body_xml=row[3].encode('utf-8'),
                )
    else:
        os.system('open {0}'.format(SKYPE_APP))
        # Wait some time wile Skype is loading and cleaning up it's database
        time.sleep(WAIT_AFTER_START)
        for user in get_skype_users():
            conn = sqlite3.connect(os.path.join(SKYPE_DIR, user, 'main.db'))
            c = conn.cursor()
            c.executescript(SQL_PATCH)
            conn.commit()
            conn.close()
