import json
import requests
import base64
import os

import datetime
last_event_time = datetime.datetime.now()
# 5 minutes
if last_event_time < datetime.datetime.now()-datetime.timedelta(seconds=300):
    print "Go"


url = "http://154.0.13.81:8080";
headers = {'content-type': 'application/json'}
auth_payload = {'email': 'coetzeel@live.co.za', 'password': '900825'}

response = requests.post(url + '/auth', data=json.dumps(auth_payload), headers=headers)
json_res = response.json()
token = json_res['token']

#with open("intrusion.png", "rb") as image_file:
    #encoded_string = base64.b64encode(image_file.read())
    #event_payload = {"image": encoded_string}
    #response = requests.post(url + '/events?token=' + token, data=json.dumps(event_payload), headers=headers)
    #json_res = response.json()
    #print(json_res)
    #os.remove("intrusion.png")

