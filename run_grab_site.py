#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      User
#
# Created:     10-12-2018
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
import subprocess
import shutil
# Remote libraries
import requests
import requests.exceptions
# local
import common
import make_cookie
import dev_config as config# For my personal development use
##import config# For disribution use

def check_if_logged_in(req_ses):
    #TODO
    pass



def find_blog_name(blog_url):# TODO
    name_search = re.search(r'[^\.\\/]\.tumblr\.com', blog_url)
    return blog_name


def run_grab_site_one_blog(blog_name, blog_url, username, base_temp_dir, base_done_dir, cookies_path):# TODO
    """Setup, run, and cleanup for one tumblr blog download through grab-site"""
    logging.info('Saving blog: {0}'.format(blog_url))
    item_name = '{blog_name}.u{username}'.format(blog_name=blog_name, username=username)
    item_temp_dir = os.path.join(base_temp_dir, item_name)
    item_done_dir = os.path.join(base_done_dir, item_name)
    item_warc_dir = os.path.join(item_temp_dir, 'warc')


    if (item_temp_dir):# Ensure temp dir exists
        if not os.path.exists(item_temp_dir):
            os.makedirs(item_temp_dir)
    assert(os.path.exists(item_temp_dir))

    if not os.path.exists(item_warc_dir):# Ensure warc dir exists
        os.makedirs(item_warc_dir)
    assert(os.path.exists(item_warc_dir))

    # Ensure expected files exist
    assert(os.path.exists(item_temp_dir))
    assert(os.path.exists(item_warc_dir))
    assert(os.path.exists(ignores_path))
    assert(os.path.exists(cookies_path))

    # Setup grab-site command
    gs_command = (''
        +'grab-site'# Command name
        +' --no-offsite-links'
        +' --dir="{td}"'.format(td=item_temp_dir)
        +' --finished-warc-dir="{wd}"'.format(wd=item_warc_dir)
        +' --ua "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0 but not really nor Googlebot/2.1"'
        +' --igsets=misc,singletumblr'
        +' --import-ignores={ign_p}'.format(ign_p=ignores_path)
        +' --wpull-args=--load-cookies={cp}'.format(cp=cookies_path)
        +' --delay=100-250'
        +' --concurrency=8'
    )

    # Run grab-site for blog
    logging.info('Running command: {0!r}'.format(gs_command))
    try:
        subprocess.check_call(gs_command)
        return_code = 0# If we didn't throw an exception it was 0
    except subprocess.CalledProcessError, err:
        return_code=err.returncode
    logging.debug('Command returned {0!r}'.format(return_code))

    # Validate run succeeded
    # TODO
    # Check command return code
    if (return_code != 0):
        pass# TODO: Handle error case
    # Check for expected files


    # Move files to final location
    # Prepare location
    if (item_done_dir):# Ensure done dir exists
        if not os.path.exists(item_done_dir):
            os.makedirs(item_done_dir)
    assert(os.path.exists(item_done_dir))# This folder should exist by this point.
    logging.info('Saved blog: {0}'.format(blog_url))

    # Move from temp to done
    logging.debug('Moving files from {0!r} to {1!r}'.format(item_temp_dir, item_done_dir))
    shutil.move(src=item_temp_dir, dst=item_done_dir)

    # Cleanup
    logging.debug('Cleaning up')
    # TODO
    # Remove temp dir
    logging.info('Finished saving blog {0!r}'.format(blog_name))
    return




def check_if_grab_site_active(grab_site_port=29000):
    res = requests.get('localhost:{0}'.format(grab_site_port))
    print res.content
    return True


def start_grab_site_server():
    logging.info('Ensuring grab-site server is running')
    # Check if server already running
    gs_server_running = check_if_grab_site_active(grab_site_port=29000)
    if gs_server_running:
        logging.info('gs-server already running, no need to start it')
        return

    # If not running, start server
    gs_server_command = (
        'gs-server'
    )
    logging.info('Running command: {0!r}'.format(gs_server_command))
    try:
        subprocess.check_call(gs_server_command)
        return_code = 0# If we didn't throw an exception it was 0
    except subprocess.CalledProcessError, err:
        return_code=err.returncode
    logging.debug('Command returned {0!r}'.format(return_code))
    logging.info('Finished starting gs-server')
    return


def download_from_list():
    #TODO
    pass


def main():
    # Get cookie
    make_cookie.make_cookie(
        cookie_path=config.cookie_path,
        email=config.email,
        username=config.username,
        password=config.password
    )
    # Run grab-site
    start_grab_site_server()
    #
    return


if __name__ == '__main__':
    common.setup_logging(os.path.join("debug", "run_grab_site.log.txt"))# Setup logging
    try:
        main()
    # Log exceptions
    except Exception, e:
        logging.critical(u"Unhandled exception!")
        logging.exception(e)
    logging.info(u"Program finished.")
