#!/usr/bin/env python

import os
import sys
import re
import json
import requests
import dns.query
import dns.update
import dns.tsigkeyring

def keyring_from_file(filename):
    d = {}
    with open(filename) as fd:
        for line in fd.readlines():
            words = line.split()
            if len(words) < 2: continue
            k = words[0]
            v = words[1].strip(";").strip('"')
            d[k] = v
    return dns.tsigkeyring.from_text({
            d["key"] : (d["algorithm"], d["secret"] )
            })

def clean_hostname(name):
    return re.sub('[^a-zA-Z0-9\-]', '', name)

def set_reflector(keyring, name,refobj):
    zone = "m17ref.tarxvf.tech."
    update = dns.update.Update(zone, keyring=keyring)
    refname = clean_hostname(name)
    port = int(refobj["Port"])
    if refobj["IPV4"]:
        refhost = refobj["IPV4"]
        update.replace('%s'%(refname), 10, 'a', "%s"%(refhost))
    if refobj["IPV6"]:
        refhost = refobj["IPV6"]
        update.replace('%s'%(refname), 10, 'aaaa', "%s"%(refhost))
    update.replace('_m17ref._udp.%s'%(refname), 10, 'srv', "20 20 %d %s.%s"%(port,refname,zone))
    update.replace('%s'%(refname), 10, 'TXT', "%s %s"%(refobj["Sponsor"], refobj["URL"]))
    #have to use rrset for replace, can't have multiple replaces in a row naturally xD
    return dns.query.tcp(update, "75.127.15.63")

if __name__ == "__main__":
    refsurl = "https://m17project.org/m17refl.json"
    keyring = keyring_from_file("ddns.key")
    # response = set_reflector(keyring, "M17-USA", {
                # "URL": "https://m17-033.dyndns.org/",
                # "IPV4": "46.226.178.84",
                # "IPV6": None,
                # "Port": 17000,
                # "Sponsor": "IW5EDX",
                # "Country": "Italy"
            # })
    reflectors = requests.get(refsurl).json()
    for ref in reflectors["m17refl"]:
        for refname,refobj in ref.items():
            response = set_reflector(keyring, refname, refobj)
            print(response)
