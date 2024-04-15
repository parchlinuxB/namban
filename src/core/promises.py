import os
from .basePromise import base_promise
class resolved(base_promise):
    def __init__(self, path):
        self.path = path
    def handle(self):
        os.replace(self.path, "/etc/systemd/resolved.conf")
    