
import os
import settings
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


def checkStartupService():
    os.system(
        'systemctl enable namban-startup-check'
    )