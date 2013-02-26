Skype like a pro
================
People deleting significant information from their Skype messages are annoying.
This app is intended to show deleted and edited Skype messages.
Currently it is available only for Mac.

Usage
----------------
Download "skypelikeapro.py" script. Now you should run Skype via
    ./skypelikeapro.py
instead of original Skype executable.

Also you can run this script if Skype already started.

Also you can build app with
    python setup.py py2app
put it in your "Applications" folder and run as normal app.

To show deleted and edited messages run:
    ./skypelikeapro.py --show
You'll see last 10 messages.
If you want more, just open Skype db and explore "skypelog" table.

Realisation
----------------
Skype stores all message history in sqlite db. Every time somebody edits or deletes
his message, Skype updates message table. This application inserts sql trigger
on updating this table to save original messages.
Skype cleans odd tables at bootstrap, so we need to create log table each time Skype starts.

Notes
----------------
This app patches Skype db, so don't forget to backup it, because I have no
responsibilities for any damage this app can make to you, your computer, your life and your death.

All logged messages are deleted every time you launch Skype.