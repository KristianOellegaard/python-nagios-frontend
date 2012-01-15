import argparse
from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.resource import Resource
import os
from balbec.jsonhandler import JSONHandler
from balbec.xmlhandler import XmlHandler

CWD = os.getcwd()

class StatusPage(Resource):
    isLeaf = True
    def render_GET(self, request):
        if request.received_headers["accept"] == "text/xml":
            handler = XmlHandler(CWD)
            output = handler.xml()
        elif request.received_headers["accept"] == "application/json":
            handler = JSONHandler(CWD)
            output = handler.json()
        else:
            output = open(os.path.join(CWD, "static/index.html")).read()
        return output

def main():
    parser = argparse.ArgumentParser(description='Run an instance of balbec.')
    parser.add_argument('--port', dest='www_port', default=8880, help='Port for the webserver')
    args = parser.parse_args()

    resource = StatusPage()
    factory = Site(resource)
    reactor.listenTCP(int(args.www_port), factory)
    reactor.run()