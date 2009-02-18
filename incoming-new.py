#! /usr/bin/python
import sys, re, time, datetime, random
from datetime import datetime
from time import gmtime
from django.core.management import setup_environ
import settings
setup_environ(settings)

from django.db import models, transaction
from email.Parser import Parser
from django.conf import settings
from django.db import connection

from www.main.models import Dictionary, Questions, User, Submitted, PendingEvents
from www.util.sms import SMS

logfile = open("/var/wordisms/log/incoming", "a+")
def logger(message):
    message = time.strftime("%m\%d\%Y %H:%M:%S", time.gmtime()) + " " + message
    logfile.write("%s\n" % message)
    print "%s" % message
logger("Entering incoming.py")

def get_plaintext(email_message):
    for part in email_message.walk():
        if part.get_content_type() == 'text/plain':
            return part.get_payload()
    raise Exception, ("Message payload not found: '%s'" % (email_message))

def validate_command(plaintext):
    if plaintext in ['1', '2', '3', '4', 'signup', 'stats', 'help', 'howto', 'quit']:
        return plaintext
    raise Exception, ("invalid command: '%s'" % plaintext)

def parse_command(command):
    tokens = command.split()
    return [ tokens[0] , tokens[1:] ]

def get_sender(email_message):
    try:
        return re.findall( re.compile("[-a-zA-Z0-9._]+@[-a-zA-Z0-9_]+.[a-zA-Z0-9_.]+"), email_message.get('From') )[0]
    except Exception:
        raise Exception, ("Invalid email address in: '%s'" % (email_message.get('From')))


        
