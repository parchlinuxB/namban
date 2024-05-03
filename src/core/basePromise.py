import os
import settings
import json
import hashlib
class base_promise:
    def __init__(self, **d) -> None:
        for name, v in d.items():
            setattr(self,name,v)
        dist = self.dump2file()
        fp = settings.PROMISES_PATH/(hashlib.sha256(bytes(dist,"UTF-8")).hexdigest() + ".promise")
        self.filePath = fp
        f = open(fp, "w+")
        f.write(
            json.dumps( {"name":type(self).__name__ ,"dist":dist} )
        )
        f.close()
        os.chmod(fp, 0o400)
    subs = []
    fields = []
    def handle(self):
        os.remove(self.filePath)
    def dump2file(self):
        d = {}
        for f in self.fields:
            d[f] = getattr(self,f)
        return json.dumps(d)
    @classmethod
    def loadfromfile(cls,data):
        d = json.loads(data)
        obj = cls(**d)
        return obj
    def __init_subclass__(cls) -> None:
        base_promise.subs.append(cls)
    @classmethod
    def FindPromiseClass(cls, name):
        try:
            return list(filter(lambda c:c.__name__ == name,cls.subs))[0]
        except:
            return