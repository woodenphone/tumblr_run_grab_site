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
import os


# Login credentials
email = ''# Tumblr account email
username = ''# Tumblr account username
password = ''# Tumblr account password


cookie_path = os.path.join(os.getcwd(), 'temp', 'cookie.txt')# Location to put the cookie file

# Todo list
list_file_path = os.path.join(os.getcwd(), 'urls.txt')# List of tumblr blogs to save

# Download paths
base_temp_dir = os.path.join(os.getcwd(), 'temp')# Where things are put while they are being worked on
base_done_dir = os.path.join(os.getcwd(), 'done')# Where things are moved once they are finished

# Configuration files
ignores_path = os.path.join(os.getcwd(), 'ignore_sets')

grab_site_port = 29000


def main():
    pass

if __name__ == '__main__':
    main()
