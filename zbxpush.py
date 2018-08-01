#!/usr/bin/env python

import socket
import sys

def main():
    args = sys.argv
    zbx_to = args[1]
    zbx_msg = args[2]
    client_port = 10052

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(bytes(zbx_msg), (zbx_to, client_port))

if __name__ == "__main__":
    main()
