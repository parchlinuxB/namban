import os
import settings
import sys

def isSocketOpen(socketPath):
    try:
        os.unlink(socketPath)
        return False
    except OSError:
        return os.path.exists(socketPath)

def runApp(req):
    f = open(settings.APP_LOCK_PATH, "w+")
    f.write(str(os.getpid()))
    f.close()
    err = 1
    if 'uid' in req: ...
        # os.setuid(int(req['uid'])) 
    if 'display' in req :
        os.environ['DISPLAY'] = req['display']
    try:
        import application
        err = application.main()
    finally:
        os.remove(settings.APP_LOCK_PATH)
        sys.exit(err)
def startApp(req):
    if os.path.exists(settings.APP_LOCK_PATH):
        pid = open(settings.APP_LOCK_PATH,'r').read().strip()
        print("Application already is running in pid: "+pid, file=sys.stderr)
        return False
    import multiprocessing as mp
    mp.Process(target=lambda:runApp(req)).start()
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

def parseRequest(bin):
    dic = {
        b"\x01":"uid",
        b"\x02":"display"
    }
    req = {}
    corsur = None
    iter = 0
    while True:
        try:
            l = bin[iter:iter+1]
            if l == b"\x00":
                break
            if corsur :
                if l != corsur:
                    req[dic[corsur]] = req.get(dic[corsur],'') + l.decode()
                else:
                    corsur = None
            else :
                if l in dic:
                    corsur = l
        except Exception as e:
            break
        finally:
            iter += 1
    return req


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
            if data[:1] == b"\x04":
                print("new connection:")
                if data[1:2] == b"\x00":
                    print("    start app")
                    try:
                        req = parseRequest(data[2:])
                        print(req)
                        if startApp(req):
                            print('    app started')
                        else:
                            print('    launch app failed')
                    except:
                        print('bad request!')
                print('close connection')
        finally:
            conn.close()
if __name__ == "__main__":
    daemon()