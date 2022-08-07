from asyncio.log import logger
from genericpath import isfile
import logging
from telegram_handler import TelegramLoggingHandler
import os
import time
import sys
import json

# logger definition
logger = logging.getLogger('core')

# to take file extancion
def get_file_ext(file_path):
     file_ext = file_path.split('.')[-1].lower()
     return file_ext

# get list pf all filles 
def get_downloads_filelist(target_dir):
    user_file_list = []

    for fs_object_name in os.listdir(target_dir):
        fs_object_path = os.path.join(target_dir, fs_object_name)
        if os.path.isfile(fs_object_path):
            user_file_list.append(fs_object_path)
    return user_file_list

# that's create dir of there are no one 
def make_dir(dir_root, dir_name):
    dir_path = os.path.join(dir_root, dir_name)
    if not os.path.isdir(dir_path): # same with !=
        logger.debug(f'Dir has been created {dir_name}')
        os.mkdir(dir_path)
        logger.debug(f'That\'s dir is already exist {dir_name}')
    return dir_path

# to transport file from dir to dir
def move_file(src_path, destination_path):
    import shutil 
    try:
        shutil.move(src_path, destination_path)
        logger.debug(f'{os.path.basename(src_path)} is moving to {destination_path}') 
    except Exception as e:
        logger.error(f'Exception name: {e}')

# home key inspector
def get_user_home_key():
    logger.info(f'Using platform: {sys.platform}')
    if sys.platform in ('linux', 'darwin'):
        user_home_key = 'HOME'
    elif sys.platform == 'win32':
        user_home_key = 'USERPROFILE'
    else: 
        user_home_key = None
    return user_home_key

# scaning all dirs for our list
def scan_dir(dir_mapping, user_root): 
    user_file_list = get_downloads_filelist(user_root)       
    for user_file_path in user_file_list:
        file_ext = get_file_ext(user_file_path)
        for dir_name in dir_mapping:
            target_dir = make_dir(user_root, dir_name)
            if file_ext in dir_mapping[dir_name]:
                file_name = os.path.basename(user_file_path)
                destination_file_path = os.path.join(target_dir, file_name)
                move_file(user_file_path, destination_file_path)
                print(f"{file_ext.upper()} {user_file_path=}  {target_dir}") # mindstorm 

# telegram send message handler
def logs_for_telegram_handlers(token, chat_id):
    try:
        telegram_log_handler = TelegramLoggingHandler(token, chat_id)
        logger.addHandler(logging.StreamHandler())
        logger.addHandler(telegram_log_handler)
    except Exception as e:
        logger.info(f"Exception definition is like: {e}")

# for delay function
def do_sleep(delay):
    logger.info(f'Sleeping for {delay} seconds')
    time.sleep(delay)

# for chancge dir with your data
def read_config(file_path):
    if os.path.isfile(file_path):
        settings_json = open(file_path)
        data = json.load(settings_json)
    else:
        settings_json = open('settings.json')
        data = json.load(settings_json)
    return data
       