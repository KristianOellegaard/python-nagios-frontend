import simplejson as json
from lxml import objectify
from balbec.objects import Hostgroup
from balbec.xmlhandler import XmlHandler, SERVICE_UNKNOWN, serviceStatus, hostStatus

class ObjectJSONEncoder(json.JSONEncoder):
    """
    A specialized JSON encoder that can handle simple lxml objectify types
       >>> from lxml import objectify
       >>> obj = objectify.fromstring("<Book><price>1.50</price><author>W. Shakespeare</author></Book>")
       >>> objectJSONEncoder().encode(obj)
       '{"price": 1.5, "author": "W. Shakespeare"}'

       From: http://stackoverflow.com/questions/471946/how-to-convert-xml-to-json-in-python
    """
    def default(self,o):
        if o.__iter__:
            returnlist = []
            for x in o:
                returnlist.append(x)
            return returnlist
        if isinstance(o, objectify.IntElement):
            return int(o)
        if isinstance(o, objectify.NumberElement) or isinstance(o, objectify.FloatElement):
            return float(o)
        if isinstance(o, objectify.ObjectifiedDataElement):
            return str(o)
        if hasattr(o, '__dict__'):
            #For objects with a __dict__, return the encoding of the __dict__
            print "dict", o.__dict__
            return o.__dict__
        print type(o)
        return json.JSONEncoder.default(self, o)

class JSONHandler(XmlHandler):
    def json(self):
        maps, backend = self.readConfig()
        dt = backend.getLastCheck()
        lastCheck = dt.strftime('%s')
        dt = backend.getCurrentDateTime()
        currentTime=dt.strftime('%s')
        json_dict = {}
        json_dict["updated_at"] = lastCheck
        json_dict["maps"] = []
        for map in maps:
            groups = self.getFilteredGroups(backend, map.expression)
            group_list = []
            for group in groups:
                if group.show == False:
                    continue
                if len(group.hostObjectIds) == 0:
                    continue
                group.hosts = backend.getHosts(group)
                group_dict = {}
                if isinstance(group, Hostgroup): group_dict["type"] = "hostgroup"
                else: group_dict["type"] = "servicegroup"
                group_dict["name"] = group.name
                group_dict["hosts"] = []
                for host in group.hosts:
                    host_dict = {'hostname': host.hostname}
                    host_dict[group_dict["type"]] = []
                    if host.result:

                        statusText = hostStatus[host.result.status]
                        statusCode = host.result.status
                    else:

                        statusText = serviceStatus[SERVICE_UNKNOWN]
                        statusCode = SERVICE_UNKNOWN

                    if isinstance(group, Hostgroup):
                        #host_dict["status"] = ""
                        host_dict["code"] = str(statusCode)
                        host_dict["text"] = str(statusText)

                    for service in host.services:
                        service_dict = {"servicename": service.servicename}
                        if service.result:

                            statusText = serviceStatus[service.result.status]
                            statusCode = service.result.status
                        else:

                            statusText = serviceStatus[SERVICE_UNKNOWN]
                            statusCode = SERVICE_UNKNOWN

                        #service_dict["status"] = ""
                        service_dict["code"] = str(statusCode)
                        service_dict["text"] = str(statusText)
                        host_dict[group_dict["type"]].append(service_dict)
                    group_dict["hosts"].append(host_dict)
                group_list.append(group_dict)
            json_dict["maps"].append({'name': map.name, 'groups': group_list})
        return json.dumps(json_dict)