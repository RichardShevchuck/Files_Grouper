import os
import argparse
import sys
import logging
import time




parser = argparse.ArgumentParser()

parser.add_argument('-d', '--target-dir-name', type=str, default='Downloads')
parser.add_argument('-D', '--debug', action='store_const', dest='loglevel',
                    const=logging.DEBUG, default=logging.INFO)
parser.add_argument('-S', '--show-config', action='store_true')
parser.add_argument('-W', '--watch', action='store_true')

ARG = parser.parse_args()
logging.basicConfig(level=ARG.loglevel)
logger = logging.getLogger('file_manager')

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


