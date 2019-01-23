from datetime import datetime
import os
import uuid

from werkzeug.utils import secure_filename


def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        os.chmod(folder_path, os.O_RDWR)


def change_filename_with_timestamp_uuid(filename):
    fileinfo = os.path.splitext(filename)
    filename = datetime.now().strftime('%Y%m%d%H%M%S') + \
        str(uuid.uuid4().hex) + fileinfo[-1]
    return filename


def secure_filename_with_timestamp(filename):
    filename = secure_filename(filename)
    fileinfo = os.path.splitext(filename)
    filename = fileinfo[0] + '_' + datetime.now().strftime('%Y%m%d%H%M%S') + fileinfo[-1]
    return filename


def secure_filename_with_uuid(filename):
    fileinfo = os.path.splitext(filename)
    filename_prefix = secure_filename(filename[0] + '_')
    filename = filename_prefix + str(uuid.uuid4().hex)[:6] + fileinfo[-1]
    return filename


ALLOWED_IMAGE_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'bmp'])
ALLOWED_VIDEO_EXTENSIONS = set(['mp4', 'avi'])
ALLOWED_AUDIO_EXTENSIONS = set(['mp3', 'm4a'])


def check_files_extensions(filesnamelist, allowed_extensions):
    for filename in filesnamelist:
        check_state = '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in allowed_extensions
        if not check_state:
            return False
    return True
