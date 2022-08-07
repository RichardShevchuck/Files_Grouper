from email.mime import application
from itertools import tee
import json
import os
import argparse
import sys
import logging
import time
import telegram
from telegram import *
from core import *



# parser arguments creating
parser = argparse.ArgumentParser()

parser.add_argument('-d', '--target-dir-name', type=str, default='Downloads')
parser.add_argument('-D', '--debug', action='store_true')
parser.add_argument('-s', '--show-config', action='store_true')
parser.add_argument('-w', '--watch', action='store_true')
parser.add_argument('-t', '--telegram-logs', action='store_true')
parser.add_argument('-i', '--watch-interval', type=float, default=2)
parser.add_argument('-j', '--settings-setup', type=str, default='settings.json')

ARG = parser.parse_args()

# init logger name
logger = logging.getLogger('config')

# with this one you could change dir with your settings
if ARG.settings_setup:
    settings = read_config(ARG.settings_setup)

# Initialize token and chat_id
token = settings['token']
chat_id = settings['chat_id']

# Init BOT
BOT = telegram.Bot(token)

# debug statement
if  any([ARG.debug, ARG.telegram_logs]):  
    log_level = level=logging.DEBUG
else:
    log_level = logging.INFO

if ARG.telegram_logs:
    logs_for_telegram_handlers(token=token, chat_id=chat_id)


#config for logger, accorded at arguments
logging.basicConfig(level=log_level)


# all dirs and extencions 
dir_mapping = {
    'Images': ('jpg', 'png', 'tiff', 'gif', 'jpeg', 'bmp'), 
    'Audio': ('mp3', 'mp4a'), 
    'Video': ('mp4', 'avi', 'mkv'), 
    'Doc': ('pdf', 'docx', 'zip', 'txt', '7z'),
    'Programs': ('exe', 'msi'),
    'Torrents': ('torrent', ),
    'Development': ('map', 'json', 'js', 'vue', 'html', 'css')
    }

# getting user home key and compare environ with others
user_home_key = get_user_home_key()
if user_home_key == None:
    logger.error(f'Unknown platform {sys.platform}')
    sys.exit() 

user_root = os.path.join(os.environ[user_home_key], ARG.target_dir_name) 

# show mapping settings
if ARG.show_config: 
    for dir_name in dir_mapping:
        allowed_ext = ', '.join(dir_mapping[dir_name])
        logging.info(f'Directory name: {dir_name}, allowed extension: [{allowed_ext}]')
    sys.exit()

# that's make program loop
if ARG.watch:
    while True:
        do_sleep(ARG.watch_interval)
        user_file_list = get_downloads_filelist(user_root)
<<<<<<< HEAD
        scan_dir(dir_mapping, user_root)
else: # regular setup 
    scan_dir(dir_mapping, user_root)
        



# bootlepy 
# fastapi 
# pewee orm
# read about functions, byte of python, Luts, lists, all about this code, os modules, one more time FUNCTION !, os.path.join how it works
# argparse read about, do some exercises with it, one more program
# dicts methods (items, values, keys, update, pop), how to take values using keys, dict function, convert dict_mapping using dict function
# do code review, reread it one more time 
# must have, all most popular methods for lists, stings, dicts, don't forget about this stuff ()!!!!!!!! Diference between functions and methods


# move all functions to a new file(do not name file like function or etc. it could be like helpers, utils, core) Done
# make settings.json like argument, and all stuff for it make like a function (name=readconfig, return dict), Done
# do if statement for json reader Done
# do Traceback*
# all any instead of if or Done
# docker !!!!!!!!!
=======
        dir_handler( dir_mapping, user_root)
>>>>>>> 269c01da171a89e9718e453d88fc338b9bfb510c
