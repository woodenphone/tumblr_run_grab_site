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



def make_item_name(blog_name, username):
    item_name = '{blog_name}.u{username}'.format(blog_name=blog_name, username=username)
    logging.debug('item_name={0!r}'.format(item_name))
    return item_name


def find_blog_name_simple(blog_url):# TODO
    # http://lemondrop-.tumblr.com/
    # lemondrop-
    name_search = re.search('([^\.\\\/]+)\.tumblr\.com', blog_url)
    if name_search:
        blog_name = name_search.group(1)
        logging.debug('blog_name={0!r}'.format(blog_name))
        return blog_name
    else:
        return None

def find_blog_name_thorough(req_ses, blog_url):# TODO
    logging.debug('Using slower, more thorough name-finding on {0!r}'.format(blog_url))
    # Extract domain
    # 'http://nsfw.kevinsano.com'
    # 'nsfw.kevinsano.com'
    domain_search = re.search(r'(?:https?://)?([^\\/]+\.\w+)/?', blog_url)
    if domain_search:
        domain = domain_search.group(1)
        logging.debug('domain={0!r}'.format(domain))
    else:
        logging.error('Could not identify domain! Failing.')
        return None
    # Genreate archive page URL
    blog_rss_url = 'http://{0}/rss'.format(domain)
    logging.debug('blog_rss_url={0!r}'.format(blog_rss_url))
    rss_path = os.path.join('debug', 'run_grab_site.find_blog_name_thorough.rss.rss')
    # Load archive page
    rss_res = common.fetch(
        requests_session=req_ses,
        url=blog_rss_url,
        method='get',
    )
    common.write_file(# Save to file for debugging
        file_path=rss_path,
        data=rss_res.content
    )
    # Extract blog name from page
    # '<generator>Tumblr (3.0; @nsfwkevinsano)</generator>'
    # 'nsfwkevinsano'
    name_search = re.search('<generator>[^<]{0,25}@([^)<]+)\)</generator>', rss_res.content)
    if name_search:
        blog_name = name_search.group(1)
    logging.debug('blog_name={0!r}'.format(blog_name))
    return blog_name


def find_blog_name(req_ses, blog_url):
    logging.debug('Finding blog name for URL: {0!r}'.format(blog_url))
    # Simple, fast method
    blog_name = find_blog_name_simple(blog_url)
    if not blog_name:
        # Slower alternate method
        blog_name = find_blog_name_thorough(req_ses, blog_url)
    logging.debug('Identified blog name as {0!r}'.format(blog_name))
    return blog_name


def assert_paths_exist(paths):
    """For better clarity than just asserts.
    This way it gives an error message showing what path was supposed to be found"""
    for current_path in paths:
        if not os.path.exists(current_path):
            logging.error('Path was expected to exist but doesnt: {0}'.format(current_path))
            raise ValueError()
    return


def run_grab_site_one_blog(req_ses, blog_name, blog_url, username,
    item_name, item_temp_dir, item_done_dir,
    item_warc_dir, cookie_path, ignores_path):# TODO
    """Setup, run, and cleanup for one tumblr blog download through grab-site"""
    logging.info('Saving blog: {0}'.format(blog_url))

    if (item_temp_dir):# Ensure temp dir exists
        if not os.path.exists(item_temp_dir):
            os.makedirs(item_temp_dir)
    assert(os.path.exists(item_temp_dir))

    if not os.path.exists(item_warc_dir):# Ensure warc dir exists
        os.makedirs(item_warc_dir)
    assert(os.path.exists(item_warc_dir))

    # Ensure expected files exist
    assert_paths_exist(paths=[
        item_temp_dir,
        item_warc_dir,
        ignores_path,
        cookie_path
    ])

    # Setup grab-site command
    gs_command = (''
        +'grab-site'# Command name
        +' --no-offsite-links'
        +' --dir="{td}"'.format(td=item_temp_dir)
        +' --finished-warc-dir="{wd}"'.format(wd=item_warc_dir)
        +' --ua "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0 but not really nor Googlebot/2.1"'
        +' --igsets=misc,singletumblr'
        +' --import-ignores="{ign_p}"'.format(ign_p=ignores_path)
        +' --wpull-args=--load-cookies="{cp}"'.format(cp=cookie_path)
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
    try:
        # Attempt to load job tracker page
        res = requests.get('http://localhost:{0}'.format(grab_site_port))
        # Could load page
        html = res.content
        return True
    except requests.ConnectionError, err:
        # Could not load page
        return False
    # Still didn't load the page, but I don't know how execution flow would reach here.
    return False


def start_grab_site_server(grab_site_port):
    logging.info('Ensuring grab-site server is running')
    # Check if server already running
    gs_server_running = check_if_grab_site_active(grab_site_port=grab_site_port)
    if gs_server_running:
        logging.info('gs-server already running, no need to start it')
        return

    # If not running, start server
    # TODO : Make this be able to start gs-server
    gs_server_command = (
##        'gs-server'
##        'bash start_gs_server.sh'
        'gs-server >/dev/null 2>&1'
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


def download_from_list(req_ses, list_file_path, username,
    cookie_path, ignores_path, base_temp_dir, base_done_dir,
    ):
    logging.info('Finished saving blogs from list file: {0}'.format(list_file_path))
    with open(list_file_path, 'ru') as lf:
        line_counter = 0
        for line in lf:
            line_counter += 1
            logging.debug('Line {0}: {1!r}'.format(line_counter, line))
            if line[0] in ['\n', '\r', '#']:# Skip empty lines and comments
                continue
            clean_line = line.lstrip().rstrip()
            # Get blog name from URL
            blog_name = find_blog_name(req_ses, blog_url=clean_line)
            if (not blog_name):
                logging.info('Could not get a blog name, skipping this line')
                continue
            # Make blog base url
            blog_url = 'https://{0}.tumblr.com/'.format(blog_name)
            logging.debug('blog_url={0!r}'.format(blog_url))
            # Generate item name
            item_name = make_item_name(blog_name=blog_name, username=username)
            # Generate item paths
            item_temp_dir = os.path.join(base_temp_dir, item_name)
            item_done_dir = os.path.join(base_done_dir, item_name)
            item_warc_dir = os.path.join(item_temp_dir, 'warc')

            # Check if already saved
            if os.path.exists(item_done_dir):
                logging.info('Item already saved, skipping this line')

            # Run grab-site
            run_grab_site_one_blog(
                req_ses=req_ses,
                blog_name=blog_name,
                blog_url=blog_url,
                username=username,
                item_name=item_name,
                item_temp_dir=item_temp_dir,
                item_done_dir=item_done_dir,
                item_warc_dir=item_warc_dir,
                cookie_path=cookie_path,
                ignores_path=ignores_path,
            )
            logging.info('Saved blog {0!r}'.format(blog_url))
            continue
    logging.info('Finished saving {count} lines from list file'.format(count=line_counter))
    return


def save_blog_list():
    # Get cookie
    req_ses = make_cookie.make_cookie(
        cookie_path=config.cookie_path,
        email=config.email,
        username=config.username,
        password=config.password
    )


    # Run grab-site
    start_grab_site_server(grab_site_port=config.grab_site_port)
    #
    find_blog_name_thorough(req_ses, blog_url='http://jayisbutts.com/')
    # Work over list
    download_from_list(
        req_ses=req_ses,
        list_file_path=config.list_file_path,
        username=config.username,
        cookie_path=config.cookie_path,
        ignores_path=config.ignores_path,
        base_temp_dir=config.base_temp_dir,
        base_done_dir=config.base_done_dir,
    )
    return


def dev():
    #
    find_blog_name(req_ses, blog_url='http://lemondrop-.tumblr.com/')
    find_blog_name(req_ses, blog_url='http://nsfw.kevinsano.com')
    #
    return


def main():
    save_blog_list()


if __name__ == '__main__':
    common.setup_logging(os.path.join("debug", "run_grab_site.log.txt"))# Setup logging
    try:
        main()
    # Log exceptions
    except Exception, e:
        logging.critical(u"Unhandled exception!")
        logging.exception(e)
    logging.info(u"Program finished.")
