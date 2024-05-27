import sys
DEBUG = '--release' not in sys.argv

_imps = []
def makeSureExists(p):
    _imps.append(p)
    return p

from pathlib import Path
base = Path(__file__)
PACKAGE_NAME = 'com.parchlinux.namban'
WINDOW_TITLE = 'namban'
APP_DATA_FILE = "./nambanAppdata.json" if DEBUG else "/etc/namban/config.json"
SOCKET_PATH = Path("/tmp/namban.sock")
APP_LOCK_PATH = Path("/tmp/namban.lck")
APP_FILES_PATH = makeSureExists(Path("/usr/share/namban"))
OLD_CONFS_PATH = makeSureExists(APP_FILES_PATH/'oldconffiles')
PROMISES_PATH = makeSureExists(APP_FILES_PATH/'promises')