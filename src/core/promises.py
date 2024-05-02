import os
from .basePromise import base_promise
class resolvd(base_promise):
    fields = ['path']
    def __init__(self, path="",**d):
        super().__init__(path=path,**d)
    def handle(self):
        os.system(f'mv {self.path} /etc/systemd/resolved.conf')
        super().handle()
class resolv_conf(base_promise):
    fields = ['path']
    def __init__(self, path="",**d):
        super().__init__(path=path,**d)
    def handle(self):
        os.system(f'mv {self.path} /etc/resolv.conf')
        super().handle()
