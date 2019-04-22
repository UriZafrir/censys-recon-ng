from recon.core.module import BaseModule

from censys.ipv4 import CensysIPv4
from censys.base import CensysException

class Module(BaseModule):
    meta = {
        'name': 'Censys Hosts by Name',
        'author': 'J Nazario',
        'description': 'Finds all IPs for a given hostname. Updates the "hosts" and "ports" tables.',
        'query': 'SELECT DISTINCT host FROM hosts WHERE host IS NOT NULL',
    }

    def module_run(self, hosts):
        api_id = self.get_key('censysio_id')
        api_secret = self.get_key('censysio_secret')
        c = CensysIPv4(api_id, api_secret)
        IPV4_FIELDS = [ 'ip', 'protocols', 'location.country', 
                        'location.latitude', 'location.longitude']        
        for host in hosts:
            self.heading(host, level=0)
            try:
                payload = [ x for x in c.search('a:{0}'.format(host), IPV4_FIELDS) ]
            except CensysException:
                continue
            for result in payload:
                self.add_hosts(host=host, 
                               ip_address=result['ip'], 
                               country=result['location.country'],
                               latitude=result['location.latitude'], 
                               longitude=result['location.longitude'])
                for protocol in result['protocols']:
                    port, service = protocol.split('/')
                    self.add_ports(ip_address=result['ip'], port=port, protocol=service)