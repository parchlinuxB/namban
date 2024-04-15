import json
class base_promise:
    def __init__(self, **d) -> None:
        for name, v in d.items():
            setattr(self,name,v)
    subs = []
    fields = []
    def handle(self): ...
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