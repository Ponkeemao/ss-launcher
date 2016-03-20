#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- date: 2016-03-19 23:21 -*-

import json
import os
import re
import subprocess

import biplist
import requests
from bs4 import BeautifulSoup

URL = 'http://www.ishadowsocks.net'
HEADERS = {
    'User-Agent':
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) ' +
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36'
}
PLIST_PATH = os.path.expanduser('~/Library/Preferences/clowwindy.ShadowsocksX.plist')


def get_config(data):
    profiles = []
    soup = BeautifulSoup(data, 'lxml')
    pattern = re.compile(r'(.*):(.*)')

    for element in soup.select('#free > div > div > div')[1:]:
        children = element.select('h4')
        status = children[4].select('font')
        if status[0]['color'] == 'red':
            continue
        server = re.sub(pattern, r'\2', children[0].text).lower()
        server_port = int(re.sub(pattern, r'\2', children[1].text))
        password = re.sub(pattern, r'\2', children[2].text)
        method = re.sub(pattern, r'\2', children[3].text)
        keys = ['server', 'server_port', 'password', 'method', 'remarks']
        values = [server.lower(), server_port, password, method, server.lower()]
        profiles.append(dict(zip(keys, values)))
    return dict(profiles=profiles, current=1)


def update_plist_with_config(path, config):
    try:
        plist_obj = biplist.readPlist(path)
    except (biplist.InvalidPlistException, biplist.NotBinaryPlistException) as err:
        print("Not a plist: {}".format(err))
    else:
        plist_obj['config'] = json.dumps(config).encode()
        plist_obj['ShadowsocksIsRunning'] = True
        plist_obj['ShadowsocksMode'] = 'global'
        plist_obj['public server'] = False
        plist_obj['proxy encryption'] = config['profiles'][config['current']]['method']
        plist_obj['proxy ip'] = config['profiles'][config['current']]['server']
        plist_obj['proxy password'] = config['profiles'][config['current']]['password']
        plist_obj['proxy port'] = str(config['profiles'][config['current']]['server_port'])
        try:
            biplist.writePlist(plist_obj, path)
        except (biplist.InvalidPlistException, biplist.NotBinaryPlistException) as err:
            print("Something bad happened: {}".format(err))


def terminate_application():
    command = 'killall ShadowsocksX'
    subprocess.call(command.split(), shell=False)


def defaults_read():
    command = 'defaults read ' + PLIST_PATH
    subprocess.call(command.split(), shell=False)


def launch_application():
    command = '/opt/homebrew-cask/Caskroom/shadowsocksx/2.6.3/ShadowsocksX.app/Contents/MacOS/ShadowsocksX'
    subprocess.call(command.split(), shell=False)


if __name__ == '__main__':
    terminate_application()
    html = requests.get(URL, headers=HEADERS).text
    config_obj = get_config(html)
    update_plist_with_config(PLIST_PATH, config_obj)
    defaults_read()
    launch_application()
