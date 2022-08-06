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
from telegram_handler import TelegramLoggingHandler


# Upload json and convert to tuple
settings_json = open('settings.json')
data = json.load(settings_json)

# Initialize token and chat_id
token = data['token']
chat_id = data['chat_id']

# Init BOT
BOT = telegram.Bot(token)

# parser arguments creating
parser = argparse.ArgumentParser()

parser.add_argument('-d', '--target-dir-name', type=str, default='Downloads')
parser.add_argument('-D', '--debug', action='store_true')
parser.add_argument('-S', '--show-config', action='store_true')
parser.add_argument('-W', '--watch', action='store_true')
parser.add_argument('-T', '--telegram-logs', action='store_true')

ARG = parser.parse_args()

logger = logging.getLogger('file_manager')

def logs_for_telegram_handlers(token, chat_id, logger):
    try:
        telegram_log_handler = TelegramLoggingHandler(token, chat_id)
        logger.addHandler(logging.StreamHandler())
        logger.addHandler(telegram_log_handler)
    except Exception as e:
        logger.info(f"Exception definition is like: {e}")

# debug statement
if ARG.debug: 
    log_level = level=logging.DEBUG
elif ARG.telegram_logs:
    log_level = logging.DEBUG
    logs_for_telegram_handlers(token=token, chat_id=chat_id, logger=logger)
else:
    log_level = logging.INFO
    
logging.basicConfig(level=log_level)

dir_mapping = {
    'Images': ('jpg', 'png', 'tiff', 'gif', 'jpeg', 'bmp'), 
    'Audio': ('mp3', 'mp4a'), 
    'Video': ('mp4', 'avi', 'mkv'), 
    'Doc': ('pdf', 'docx', 'zip'),
    'Programs': ('exe', 'msi'),
    'Torrents': ('torrent', ),
    'Development': ('map', 'json', 'js', 'vue', 'html', 'css')
    }


def get_user_home_key():
    logger.info(f'Using platform: {sys.platform}')
    if sys.platform in ('linux', 'darwin'):
        user_home_key = 'HOME'
    elif sys.platform == 'win32':
        user_home_key = 'USERPROFILE'
    else: 
        user_home_key = None
    return user_home_key

user_home_key = get_user_home_key()
if user_home_key == None:
    logger.error(f'Unknown platform {sys.platform}')
    sys.exit() 

user_root = os.path.join(os.environ[user_home_key], ARG.target_dir_name) 

def get_file_ext(file_path):
     file_ext = file_path.split('.')[-1].lower()
     return file_ext


def get_downloads_filelist(target_dir):
    user_file_list = []

    for fs_object_name in os.listdir(target_dir):
        fs_object_path = os.path.join(target_dir, fs_object_name)
        if os.path.isfile(fs_object_path):
            user_file_list.append(fs_object_path)
    return user_file_list


def make_dir(dir_root, dir_name):
    dir_path = os.path.join(dir_root, dir_name)
    if not os.path.isdir(dir_path): # same with !=
        logger.debug(f'Dir has been created {dir_name}')
        os.mkdir(dir_path)
        logger.debug(f'That\'s dir is already exist {dir_name}')
    return dir_path


def move_file(src_path, destination_path):
    import shutil 
    try:
        shutil.move(src_path, destination_path)
        logger.debug(f'{os.path.basename(src_path)} is moving to {destination_path}') 
    except Exception as e:
        logger.error(f'Exception name: {e}')



def dir_handler(dir_mapping, user_root): 
    user_file_list = get_downloads_filelist(user_root)       
    for user_file_path in user_file_list:
        time.sleep(2)
        file_ext = get_file_ext(user_file_path)
        for dir_name in dir_mapping:
            target_dir = make_dir(user_root, dir_name)
            if file_ext in dir_mapping[dir_name]:
                file_name = os.path.basename(user_file_path)
                destination_file_path = os.path.join(target_dir, file_name)
                move_file(user_file_path, destination_file_path)
                print(f"{file_ext.upper()} {user_file_path=}  {target_dir}") # mindstorm 

dir_handler(dir_mapping, user_root)
        
if ARG.show_config: 
    for dir_name in dir_mapping:
        allowed_ext = ', '.join(dir_mapping[dir_name])
        logging.info(f'Directory name: {dir_name}, allowed extension: [{allowed_ext}]')
    sys.exit()

if ARG.watch:
    while True:
        user_file_list = get_downloads_filelist(user_root)
        dir_handler( dir_mapping, user_root)


<<<<<<< HEAD

# bootlepy 
# fastapi 
# pewee orm
# read about functions, byte of python, Luts, lists, all about this code, os modules, one more time FUNCTION !, os.path.join how it works
# argparse read about, do some exercises with it, one more program
# dicts methods (items, values, keys, update, pop), how to take values using keys, dict function, convert dict_mapping using dict function
# import logging and use it for debug messages * Done
# watch argument for argparse if it's true code should work all the time * using while(True), time.sleep Done
# do code review, reread it one more time Done
# must have, all most popular methods for lists, stings, dicts, don't forget about this stuff ()!!!!!!!! Diference between functions and methods 
=======
>>>>>>> f648cc38a44061ee420a8972c076d1de48466cff
