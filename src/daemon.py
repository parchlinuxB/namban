import os
import settings
import sys

def isSocketOpen(socketPath):
    try:
        os.unlink(socketPath)
        return False
    except OSError:
        return os.path.exists(socketPath)

def runApp(uid):
    f = open(settings.APP_LOCK_PATH, "w+")
    f.write(str(os.getpid()))
    f.close()
    err = 1
    try:
        import application
        err = application.main(uid)
    finally:
        os.remove(settings.APP_LOCK_PATH)
        sys.exit(err)
def startApp(uid):
    if os.path.exists(settings.APP_LOCK_PATH):
        pid = open(settings.APP_LOCK_PATH,'r').read().strip()
        print("Application already is running in pid: "+pid, file=sys.stderr)
        return False
    import multiprocessing as mp
    mp.Process(target=lambda:runApp(uid)).start()
    return True
import re
import json
from core.basePromise import base_promise
def checkPromises():
    promiseFiles = os.listdir(settings.PROMISES_PATH)
    for pf in filter(lambda n: re.match(r".+\.promise",os.path.basename(n)) ,promiseFiles):
        try:
            file = open(pf,"r")
            row = file.read()
            file.close()
            js = json.loads(row)
            name = js['name']
            PromiseClass = base_promise.FindPromiseClass(name)
            promise = PromiseClass.loadfromfile(js['dist'])
            promise.handle()
        except:
            os.remove(pf)
def checkPaths():
    def makSure(f):
        if not os.path.exists(f):
            os.mkdir(f)
    for p in settings._imps:
        makSure(p)

def daemon():
    checkPaths()
    checkPromises()
    if isSocketOpen(settings.SOCKET_PATH):
        print(f"Another daemon is using {settings.SOCKET_PATH}", file=sys.stderr)
        sys.exit(1)
    print("starting namban daemon")
    import socket
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.bind(settings.SOCKET_PATH.__str__())
    sock.listen(True)
    os.chmod(settings.SOCKET_PATH, 0o777)
    print(f'listening to unix://{settings.SOCKET_PATH.__str__()}')
    while True:
        conn, addr = sock.accept()
        try:
            data = conn.recv(16)
            print(data)
            if data[:1] == b"\x04":
                print("new connection:")
                if data[1:2] == b"\x00":
                    print("    start app")
                    uid = data[2:]
                    uid = uid.decode()
                    print("    uid: "+uid)
                    uid = int(uid)
                    if startApp(uid):
                        print('    app started')
                    else:
                        print('    launch app failed')
                print('close connection')
        finally:
            conn.close()
if __name__ == "__main__":
    daemon()