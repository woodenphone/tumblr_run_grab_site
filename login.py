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





def tumblr_login(req_ses, email, username, password):
    logging.info('Logging in as {0!r}'.format(username))

    # Load front page to look normal
    logging.debug('Loading front page to prepare login attempt')
    response_1 = common.fetch(
        requests_session=req_ses,
        url='https://www.tumblr.com/login',
        method='get',
    )
    common.write_file(
        file_path=os.path.join('debug', 'login.response_1.html'),
        data=response_1.content
    )

    # Load login page
    logging.debug('Loading login page')
    response_2 = common.fetch(
        requests_session=req_ses,
        url='https://www.tumblr.com/login',
        method='get',
    )
    common.write_file(
        file_path=os.path.join('debug', 'login.response_2.html'),
        data=response_2.content
    )

    # Get key from login page
    #'<meta name="tumblr-form-key" id="tumblr_form_key" content="!1231544361914|zzONO1XougbCpvRupb561N630">'
    token_search = re.search('<meta name="tumblr-form-key" id="tumblr_form_key" content="([a-zA-Z0-9!|]+)">', response_2.content, re.IGNORECASE)
    token = token_search.group(1)

    # Perform login
    logging.debug('Sending login request')
    response_3 = common.fetch(
        requests_session=req_ses,
        url='https://www.tumblr.com/login',
        method='post',
        data={
            'determine_email': email,
            'user[email]': email,
            'user[password]': password,
            'form_key': token,
        },
        expect_status=200,
    )
    common.write_file(
        file_path=os.path.join('debug', 'login.response_3.html'),
        data=response_3.content
    )

    # Validate login worked
    logging.debug('Checking if login worked')
    response_4 = common.fetch(
        requests_session=req_ses,
        url='https://www.tumblr.com/dashboard',
        method='get',
    )
    common.write_file(
        file_path=os.path.join('debug', 'login.response_4.html'),
        data=response_4.content
    )
    # TODO
    logging.warning('Login validation still TODO')

    logging.info('Logged in as {0!r}'.format(username))
    return







def main():
    pass

if __name__ == '__main__':
    main()
