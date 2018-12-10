#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      User
#
# Created:     09-12-2018
# Copyright:   (c) User 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------
# StdLib
import time
import os
import random
import logging
import logging.handlers
import datetime
import json
import cookielib
import re
# Remote libraries
import requests
import requests.exceptions
# local
import common
from login import tumblr_login# tumblr_login(req_ses, email, username, password)
##import dev_config as config# For my personal development use
import config# For disribution use


def main():
    # Setup requests
    req_ses = requests.Session()# Setup requests session
    if (cookie_dir):
        if not os.path.exists(cookie_dir):
            os.makedirs(cookie_dir)
        assert(os.path.exists(cookie_dir))# This folder should exist by this point.
    req_ses.cookies = cookie_jar = cookielib.MozillaCookieJar(config.cookie_path)# Prepare cookiejar for later use

    # Log in
    tumblr_login(req_ses, email=config.email, username=config.username, password=config.password)

    # Save cookie to file
    req_ses.cookies.save()
    assert(os.path.exists(config.cookie_path))# File must exist at this point
    return


if __name__ == '__main__':
    common.setup_logging(os.path.join("debug", "make_cookie.log.txt"))# Setup logging
    try:
        main()
    # Log exceptions
    except Exception, e:
        logging.critical(u"Unhandled exception!")
        logging.exception(e)
    logging.info(u"Program finished.")
