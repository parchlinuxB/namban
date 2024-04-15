import os
from .basePromise import base_promise
class resolved(base_promise):
    fields = ['path']
    def __init__(self, path="",**d):
        super().__init__(path=path,**d)
    def handle(self):
        os.replace(self.path, "/etc/systemd/resolved.conf")
