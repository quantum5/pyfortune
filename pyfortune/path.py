import os
import re
import logging

logger = logging.getLogger('pyfortune')
userdata = (os.path.expanduser('~/.pyfortune') if os.name != 'nt' else
            os.path.expandvars('%APPDATA%/PyFortune'))
userdata = os.path.normpath(userdata)
fortunepath = []

def get_all_user_data():
    if os.name != 'nt':
        return

    import ctypes
    from ctypes import wintypes, windll
    
    CSIDL_COMMON_APPDATA = 35
    SHGetFolderPath = windll.shell32.SHGetFolderPathW
    SHGetFolderPath.argtypes = [wintypes.HWND, ctypes.c_int, wintypes.HANDLE,
                                wintypes.DWORD, wintypes.LPCWSTR]
    path_buf = ctypes.create_unicode_buffer(wintypes.MAX_PATH)
    result = SHGetFolderPath(0, CSIDL_COMMON_APPDATA, 0, 0, path_buf)
    return path_buf.value

def add_if_exist(array, directory):
    if os.path.isdir(directory):
        array.append(directory)

try:
    for _path in os.environ['FORTUNEPATH'].split(os.pathsep):
        add_if_exist(fortunepath, _path)
except KeyError:
    pass

add_if_exist(fortunepath, userdata)
if os.name == 'nt':
    add_if_exist(fortunepath, os.path.join(get_all_user_data(), 'fortunes'))
else:
    add_if_exist(fortunepath, '/usr/local/share/pyfortunes')
add_if_exist(fortunepath, os.path.join(os.path.dirname(__file__), 'data'))
# I will skip over the /usr fortunes because that what the distro comes with
# not what I came with. When you are not root it's hard to compile them.
# If you really want pyfortune to access them, use symlinks

def mkdir(path):
    try:
        os.makedirs(path)
    except OSError as e:
        import errno
        if e.errno != errno.EEXIST or not os.path.isdir(path):
            raise

def list_fortune(offensive=False, path=fortunepath, lang=None, include=False,
                 refile=re.compile(r'^[^\.]+$')):
    files = []
    added = set()
    def isfile(dir, file):
        if refile.match(file) is None:
            return
        file = os.path.join(dir, file)
        if os.path.isfile(file):
            return file

    if lang is not None:
        oldpath = path
        path = [os.path.join(dir, lang) for dir in oldpath]
    # Offensive = None means both, False means no offensive, True means offensive only
    if not offensive:
        for dir in path:
            try:
                for file in os.listdir(dir):
                    file = isfile(dir, file)
                    if file is not None and file not in added:
                        files.append(file)
                        added.add(file)
            except OSError as e:
                logger.error("Can't enumerate directory: %s: %s", dir, e.strerror)
    if offensive != False:
        for dir in path:
            dir = os.path.join(dir, 'off')
            if not os.path.isdir(dir):
                continue
            for file in os.listdir(dir):
                file = isfile(dir, file)
                id = 'off/%s' % file
                if file is not None and id not in added:
                    files.append(file)
                    added.add(id)
    if lang is not None and include:
        # Include the default set
        files.extend(list_fortune(offensive, oldpath))
    return files
