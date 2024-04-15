import socket
import settings
import os
import sys

if not os.path.exists(settings.SOCKET_PATH):
    print("namban daemon is not running!" ,file=sys.stderr)
    print("try this:" ,file=sys.stderr)
    print("    systemctl enable --now namban" ,file=sys.stderr)
    sys.exit(1)


uid = os.getuid()

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sock.connect(settings.SOCKET_PATH)
sock.sendall(b"\x04\x00"+bytes(str(uid),"UTF-8"))
sock.close()