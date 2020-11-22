#!/usr/bin/python

import sys
import requests
from lxml import html

# URL paths init
# WARNING: SCHEDULE_URI might change in future as the semester ends and a new one begins
# TODO: tinker with INSIS paths and find which one should be the constant through which you can access timetable even after the semester ends 
INSIS_ROOT = "https://insis.vse.cz" 
SCHEDULE_URI = "/auth/katalog/rozvrhy_view.pl?osobni=1&format=list&zobraz=Zobrazit"
AUTH_URI = "/auth/"

# Request properties
XNAME = "credential_0"
PWD = "credential_1"
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "cs;q=0.9,en-US;q=0.8,cs-CZ;q=0.7",
    "Connection": "keep-alive",
    "Host": "insis.vse.cz",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap Chromium/80.0.3987.132 Chrome/80.0.3987.132 Safari/537.36",
    "Origin": "https://insis.vse.cz",
    "Referer": "https://insis.vse.cz/auth/katalog/rozvrhy_view.pl"
}
data = {
    "login_hidden": "1",
    "destination": "/auth/",
    "auth_id_hidden": "0",
    "auth_2fa_type": "no",
    "credential_k": "",
    "credential_2": "86400"
}


# Get commandline arguments
# TODO: add null check!
xname = sys.argv[1]
pwd = sys.argv[2]
data[XNAME] = xname
data[PWD] = pwd

response1 = requests.post(INSIS_ROOT + AUTH_URI, data = data, headers = headers)
#TODO: check if (req.status_code) == 200
cookie = response1.request.headers['Cookie']
headers['Cookie'] = cookie

response2 = requests.get(INSIS_ROOT + SCHEDULE_URI, headers = headers)
tree = html.fromstring(response2.content)
elements = tree.xpath('//table[@id="tmtab_1"]/tbody/tr')

json = ''
id_counter = 1
for el in elements:
    json +=  '{\n'
    json += '  "Id": ' + str(id_counter) + ',\n'
    json += '  "Day": ' + '"' + el[0].text + '",\n'
    json += '  "From": ' + '"' + el[1].text + '",\n'
    json += '  "Until": ' + '"' + el[2].text + '",\n'
    json += '  "Ident": ' + '"' + el[3][0].text[0:6] + '",\n'
    json += '  "Course": ' + '"' + el[3][0].text[7:] + '",\n'
    json += '  "Entry": ' + '"' + el[4].text + '",\n'
    json += '  "Room": ' + '"' + el[5][0].text + '",\n'
    json += '  "Teacher": ' + '"' + el[6][0][0].text + '"\n'
    json += '},\n'
    id_counter+=1

file = open("resp.json", "w")
file.write(json[:-2])  #without last comma
file.close()
