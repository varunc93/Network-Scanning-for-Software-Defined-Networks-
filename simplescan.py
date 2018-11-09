import os
import logging
import unicodedata
from keystoneauth1.identity import v3
from keystoneauth1 import session
from keystoneauth1 import identity
import novaclient.client
import neutronclient.neutron.client
import requests
from flask import Flask, request
from flask_restful import Resource, Api
import xmltodict
import json
import glob

app = Flask(__name__)
api= Api(app)

class SimpleScan(Resource):
    def get(self,namespace,hosts):
        namespace = namespace
        hosts = hosts
        cmd = "sudo ip netns exec " + namespace + " nmap " + hosts + " -A -O -oX /opt/stack/simplescanresult/" + str(
            namespace) + ".xml"
        print(cmd)
        os.system(cmd)
        file = '/opt/stack/simplescanresult/'+str(namespace)+'.xml'
        new_j_file_name='/opt/stack/simplescanresult/jsonfile/'+str(namespace)+'.json'
        d={}
        with open(file, "rb") as f:
            d = xmltodict.parse(f, xml_attribs="True")
        with open(new_j_file_name, 'w') as jfile:
            json.dump(d, jfile, indent=4)
        with open(new_j_file_name) as data_file:
            return json.load(data_file)


api.add_resource(SimpleScan, '/SimpleScan/<string:namespace>/<string:hosts>',methods=['GET'])

if __name__ == '__main__':
        app.run(host='0.0.0.0', port=7000, debug=True)
