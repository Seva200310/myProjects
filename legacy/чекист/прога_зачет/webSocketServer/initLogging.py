#!/usr/bin/env python3
import sys
import codecs
import time
import logging

def initLogging():
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
 
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(relativeCreated)6d %(threadName)s %(message)s"
    )

