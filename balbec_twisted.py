import argparse
from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.resource import Resource
import os
from balbec.htmlhandler import HtmlHandler
CWD = os.getcwd()

class StatusPage(Resource):
    isLeaf = True
    def render_GET(self, request):
        handler = HtmlHandler(CWD)
        output = handler.html()
        return output

def main():
    parser = argparse.ArgumentParser(description='Run an instance of balbec.')
    parser.add_argument('--port', dest='www_port', default=8880, help='Port for the webserver')
    args = parser.parse_args()

    resource = StatusPage()
    factory = Site(resource)
    reactor.listenTCP(int(args.www_port), factory)
    reactor.run()