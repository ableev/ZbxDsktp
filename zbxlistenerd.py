#!/usr/bin/env python
# coding: utf-8

import ConfigParser
import socket
import sys
import platform
import os


def url_map(host, trigger):

    url = ""

    map_hosts = {
        "ErrorLogs": "http://errorlogs.lan",
        "monitoring.lan": "http://monitoring.lan/"
    }

    map_triggers = {
        "phtml": "http://{0}/{1}".format(host, trigger)
    }

    for key, value in map_hosts.iteritems():
        if host.find(key) > -1:
            url = value

    for key, value in map_triggers.iteritems():
        if trigger.find(key) > -1:
            url = value

    if not url:
        url = "ssh://{0}".format(host)

    return url


def get_os():
    uname = platform.uname()[0]
    return uname


def app_terminal_notifier(host, trigger, icon):
    url = url_map(host, trigger)
    cmd = 'terminal-notifier -group "{0} {1}" -title "{0}" -message "{1}" -open "{2}" -appIcon "{3}"'.\
        format(host, trigger, url, icon)
    print cmd
    os.popen(cmd)


def app_growl(host, trigger, icon):
    url = url_map(host, trigger)
    cmd = 'growlnotify --identifier "{0} {1}" --title "{0}" --message "{1}" ' \
          '--url "{2}" --priority 2 --sticky --image "{3}"'.\
        format(host, trigger, url, icon)
    print cmd
    os.popen(cmd)


def app_notify_send(host, trigger, icon, ttl):
    #url = url_map(host, trigger)
    cmd = 'notify-send -t "{0}" -i "{1}" "{2}" "{3}"'.\
        format(ttl, icon, host, trigger)
    print cmd
    os.popen(cmd)


def send_message(host, trigger, is_growl, icon, ttl):

    trigger = trigger.replace('"', '\\"')

    if get_os() == "Darwin":
        if is_growl:
            app_growl(host, trigger, icon)
        else:
            app_terminal_notifier(host, trigger, icon)

    if get_os() == "Linux":
        app_notify_send(host, trigger, icon, ttl)


def main():

    config = ConfigParser.ConfigParser()
    config.read("settings.cfg")
    conf = dict(config.items('ZbxDsktp'))

    ip = conf["ip"]
    port = int(conf["port"])

    try:
        if conf["growl_enabled"] == "True":
            growl_enabled = True
        else:
            growl_enabled = False
    except:
        growl_enabled = False
    try:
        popupttl = conf["popupttl"]
    except:
        popupttl = "8640000"

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip, port))

    try:
        while True:
            data, addr = sock.recvfrom(10240)
            severity, host, trigger = data.split("@@@")

            icon = "{0}/{1}.png".format(conf["icon_dir"], severity)

            triggers_ignore = [
            "usersversioncheck failed to run ",
            "usersversion is too old ",
            ]
            if trigger not in triggers_ignore:
                send_message(host, trigger, growl_enabled, icon, popupttl)

    except (KeyboardInterrupt, SystemExit):
        print "Exiting..."
        sys.exit()


if __name__ == "__main__":
    main()
