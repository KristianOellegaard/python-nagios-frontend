import argparse
from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.resource import Resource
import os
from balbec.jsonhandler import JSONHandler
from balbec.xmlhandler import XmlHandler

ROOT = lambda base : os.path.join(os.path.dirname(__file__), base).replace('\\','/')

class StatusPage(Resource):
    isLeaf = True
    config_dir = None
    def render_GET(self, request):
        if request.received_headers["accept"] == "text/xml":
            handler = XmlHandler(self.config_dir)
            output = handler.xml()
        elif request.received_headers["accept"] == "application/json":
            handler = JSONHandler(self.config_dir)
            output = handler.json()
        else:
            output = open(ROOT("static/index.html")).read()
        return output

def main():
    parser = argparse.ArgumentParser(description='Run an instance of python-nagios-frontend.')
    parser.add_argument('--port', dest='www_port', default=8880, help='Port for the webserver')
    parser.add_argument('--configdir', dest='config_dir', default="/etc/python-nagios-frontend/", help='Path to the configuration files')
    args = parser.parse_args()
    resource = StatusPage()
    resource.config_dir = args.config_dir
    factory = Site(resource)
    reactor.listenTCP(int(args.www_port), factory)
    reactor.run()