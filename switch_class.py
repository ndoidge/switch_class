"""
switch_class.py - by Nick Doidge (ndoidge@cisco.com)
----------------
A basic class definition for a switch (or device). Allows you to connect to a switch using the NXAPI and 'sessions',
this maintains session information such as cookies, so you do not have to parse this info yourself. At present these
scripts assume you are using JSON to format message bodies etc. I will write extensions for XML when I can be bothered :-D

To create a switch object, first define a dictionary in the following format:
    <dict_name> = {
        'protocol': 'http',
        'ip': '127.0.0.1',
        'port': '10180',
        'headers': {
            #Add headers if necessary
        },
        'username': '<username>',
        'password': '<password>'
    }

Note: square brackets indicate variable names - you can choose what you like as long as they conform to Python variable naming standards

Then call the switch class, specifying the dictionary you just created, the username and password)
    <switch_name> = switch(<dict_name>)

You can then perform a AAA login
    <switch_name>.aaaLogin()

Now you can perform GET and POST requests with the functions:
    <switch_name>.get(<url>)
    <switch_name.post(<url>, <body>)

Note in both cases the URL is the API path, not including the hostname/ IP/ port etc... i.e. '/api/mo/sys.json?rsp-subtree=children'
The <body> argument to the POST method should be a dictionary

Once you are finished you can logout of the switch with
    <switch_name>.aaaLogout()

As a final clean up, delete the created class
    del <switch_name>

"""

import requests
import json


class switch():

    def __init__(self, device):
        self.device = device

        #Take in the host details to produce the URL for REST requests
        self.url = '{0}://{1}:{2}'.format(self.device['protocol'], self.device['ip'], self.device['port'])

        #create the session object which allows each switch class a single session for all API calls
        self.session = requests.session()

    def aaaLogin(self):
        body = {
            "aaaUser": {
                "attributes": {
                    "name": self.device['username'],
                    "pwd": self.device['password']
                }
            }
        }

        # append the aaaLogin.json portion to create the full URL
        full_url = self.url + '/api/aaaLogin.json'

        #call the post, catch any potential errors (could be less lazy and try to identify them properly)
        try:
            response = self.session.post(full_url, json=body)
        except:
            print 'Unable to establish connectivity to the device: ' + self.device['ip']
            return 0

        if response.status_code != requests.codes.ok:
            return 0
        else:
            return 1


    def aaaLogout(self):

        body = {
		    'aaaUser' : {
			    'attributes' : {
				    'name' : self.device['username']
			    }
		    }
	    }

        #append the aaaLogout.json portion to create the full URL
        full_url = self.url + '/api/aaaLogout.json'

        #logout of the switch
        try:
            response = self.session.post(full_url, json=body)
        except:
            print 'Unable to establish connectivity to the device: ' + self.device['ip']
            return 0

        if response.status_code != requests.codes.ok:
            return response.status_code,
        else:
            return 1


    def get(self, url):
        return self.session.get(self.url + url)


    def post(self, url, body):
        return self.session.post(self.url + url, json=body)


