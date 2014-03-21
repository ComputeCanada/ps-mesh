#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import urllib2
from bs4 import BeautifulSoup


def fetchInfo(hostname):
    """ Return a dict containing these entries found on the PerfSonar's webpage:
    city, state, country, admin_name, admin_email, latitude, longitude
    """
    print 'Fetching info on', hostname
    response = urllib2.urlopen('http://' + hostname)
    soup = BeautifulSoup(response.read())
    host_table = soup.find_all('table', 'basic_table')[0]
    rows = host_table.find_all('tr')
    parsed_rows = []
    for row in rows:
        parsed_cols = []
        for col in row.find_all('td'):
            parsed_cols.append(col.string)
        parsed_rows.append(parsed_cols)
    return {
        'city': parsed_rows[2][1].split(',')[0],
        'state': parsed_rows[2][1].split(',')[1],
        'country': parsed_rows[2][1].split(',')[2],
        'admin_name': parsed_rows[5][1],
        'admin_email': parsed_rows[6][1],
        'latitude': parsed_rows[4][1].split(',')[0],
        'longitude': parsed_rows[4][1].split(',')[1]
    }


def bandwidthHostDescription(hostname, name):
    return """
  <host>
    description    {name}
    address        {hostname}

    <measurement_archive>
      type        traceroute
      read_url    http://{hostname}:8086/perfSONAR_PS/services/tracerouteMA
      write_url   http://{hostname}:8086/perfSONAR_PS/services/tracerouteCollector
    </measurement_archive>

    <measurement_archive>
      type        perfsonarbuoy/bwctl
      read_url    http://{hostname}:8085/perfSONAR_PS/services/pSB
      write_url   {hostname}:8569
    </measurement_archive>
  </host>
""".format(hostname=hostname, name=name)


def latencyHostDescription(hostname, name):
    return """
  <host>
    description    {name}
    address        {hostname}

    <measurement_archive>
      type        traceroute
      read_url    http://{hostname}:8086/perfSONAR_PS/services/tracerouteMA
      write_url   http://{hostname}:8086/perfSONAR_PS/services/tracerouteCollector
    </measurement_archive>

    <measurement_archive>
      type        perfsonarbuoy/owamp
      read_url    http://{hostname}:8085/perfSONAR_PS/services/pSB
      write_url   {hostname}:861
    </measurement_archive>

    <measurement_archive>
      type       pinger
      read_url   http://{hostname}:8075/perfSONAR_PS/services/pinger/ma
      # No 'write_url' for PingER measurement archives
    </measurement_archive>
  </host>
""".format(hostname=hostname, name=name)


def siteDescription(hostnames, name):
    """ Take a tuple of hostnames, first hostname is the bandwidth host and the
    second is the latency host. Use None as a hostname if a node is missing.
    'name' paramater is the human name for the node
    """
    if hostnames[0] is not None:
        info = fetchInfo(hostnames[0])
    else:
        info = fetchInfo(hostnames[1])

    hosts = ""
    if hostnames[0] is not None:
        hosts += bandwidthHostDescription(hostnames[0], name)
    if hostnames[1] is not None:
        hosts += latencyHostDescription(hostnames[1], name)

    return """<site>
  <location>
    city      {city}
    state     {state}
    country   {country}
    latitude  {latitude}
    longitude {longitude}
  </location>

  <administrator>
    name       {admin_name}
    email      {admin_email}
  </administrator>
{hosts}
</site>
""".format(hosts=hosts, **info)


def organization(sites, name, email, filename):
    sites_string = ""
    for site in sites:
        sites_string += siteDescription(site[0], site[1])
    s = """<organization>
  description    {name}

  <administrator>
    name       {name}
    email      {email}
  </administrator>
  {sites}
</organization>""".format(sites=sites_string, name=name, email=email)

    fo = open(filename, "wb")
    fo.write(s)
    fo.close()

if __name__ == '__main__':
    organization([
        (('bdw-ulaval.calculquebec.ca', 'lat-ulaval.calculquebec.ca'), 'Univ. Laval'),
        (('bdw-mcgill.calculquebec.ca', 'lat-mcgill.calculquebec.ca'), 'McGill Univ.'),
        (('bdw-umontreal.calculquebec.ca', 'lat-umontreal.calculquebec.ca'), 'Univ. de Montreal'),
        (('bdw-udes.ccs.usherbrooke.ca', 'lat-udes.ccs.usherbrooke.ca'), 'Univ. de Sherbrooke')],
        'Calcul-Quebec',
        'noc@calculquebec.ca',
        'sites-cq.conf')

    organization([
        (('bdw-uvic.westgrid.ca', 'lat-uvic.westgrid.ca'), 'Univ. of Victoria'),
        (('bdw-ubc.westgrid.ca', 'lat-ubc.westgrid.ca'), 'Univ. of British Columbia'),
        (('bdw-sfu.westgrid.ca', 'lat-sfu.westgrid.ca'), 'Simon Fraser Univ.'),
        (('bdw-ucalgary.westgrid.ca', 'lat-ucalgary.westgrid.ca'), 'Univ. of Calgary'),
        (('bdw-ualberta.westgrid.ca', 'lat-ualberta.westgrid.ca'), 'Univ. of Alberta'),
        (('bdw-usask.westgrid.ca', 'lat-usask.westgrid.ca'), 'Univ. of Saskatchewan'),
        (('bdw-umanitoba.westgrid.ca', 'lat-umanitoba.westgrid.ca'), 'Univ. of Manitoba')],
        'WestGrid',
        'systems@westgrid.ca',
        'sites-wg.conf')

    organization([
        (('bdw-uwo.sharcnet.ca', 'lat-uwo.sharcnet.ca'), 'Univ. of Western Ontario'),
        (('bdw-uw.sharcnet.ca', 'lat-uw.sharcnet.ca'), 'Univ. of Waterloo'),
        #(('bdw-mac.sharcnet.ca', 'lat-mac.sharcnet.ca'), 'McMaster Univ.'),  # Not responding
        #(('bdw-uog.sharcnet.ca', 'lat-uog.sharcnet.ca'), 'Univ. of Guelph'),  # Not responding
        (('bdw-utoronto.scinet.utoronto.ca', 'lat-utoronto.scinet.utoronto.ca'), 'Univ. of Toronto'),
        (('bdw.hpcvl.queensu.ca', 'lat.hpcvl.queensu.ca'), 'Queens Univ.')],
        'Sharcnet',
        'TODO',
        'sites-co.conf')

    organization([
        (('ps-bandwidth.scinet.utoronto.ca', None), 'SciNet Toronto')],
        'SciNet',
        'groer@physics.utoronto.ca',
        'sites-SciNet.conf')

    organization([
        #(('bdw-stfx.ace-net.ca', 'lat-stfx.ace-net.ca'), 'St. Francix Xavier Univ.'),  # Not responding
        #(('bdw-mta.ace-net.ca, 'lat-mta.ace-net.ca'), 'TODO'),  # Not responding
        #(('bdw-cbu.ace-net.ca', 'lat-cbu.ace-net.ca'), 'Cape Breton Univ.'),  # Not responding
        (('bdw-acadiau.ace-net.ca', 'lat-acadiau.ace-net.ca'), 'Acadia Univ.')],
        'AceNet',
        'TODO',
        'sites-AceNet.conf')

    organization([
        (('bdw-mtrl2pfs2.canarie.ca', 'lat-mtrl2pfs1.canarie.ca'), 'CANARIE Montreal'),
        (('bdw-hlfx1pfs2.canarie.ca', 'lat-hlfx1pfs1.canarie.ca'), 'CANARIE Halifax'),
        (('bdw-toro1pfs2.canarie.ca', 'lat-toro1pfs1.canarie.ca'), 'CANARIE Toronto'),
        (('sask1pfs2.canarie.ca', 'sask1pfs2.canarie.ca'), 'CANARIE Saskatoon'),  # Only one node for both services
        (('bdw-vncv1pfs2.canarie.ca', 'lat-vncv1pfs1.canarie.ca'), 'CANARIE Vancouver'),
        (('bdw-wnpg1pfs2.canarie.ca', 'lat-wnpg1pfs1.canarie.ca'), 'CANARIE Winnipeg'),
        ((None, 'otwa3pfs1.canarie.ca'), 'CANARIE Ottawa'),
        (('bdw-clgr2pfs2.canarie.ca', 'lat-clgr2pfs1.canarie.ca'), 'CANARIE Calgary')],
        'CANARIE',
        'noc@canarie.ca',
        'sites-CANARIE.conf')

    organization([
        (('pfs2-bw.klwn1.bc.net', 'pfs1-lat.klwn1.bc.net'), 'BCNET Kelowna'),
        (('pfs2-bw.srry1.bc.net', None), 'BCNET Surrey'),
        (('pfs2-bw.kmlp2.bc.net', None), 'BCNET Kamloops'),
        (('pfs2-bw.vctr1.bc.net', None), 'BCNET Victoria'),
        (('pfs2-bw.pgrg1.bc.net', None), 'BCNET Prince George')],
        'BCNET',
        'TODO',
        'sites-BCNET.conf')

    organization([
        (('bdw-uofa-edm.cybera.ca', 'lat-uofa-edm.cybera.ca'), 'Cybera Edmonton'),
        (('bdw-uofc-cgy.cybera.ca', 'lat-uofc-cgy.cybera.ca'), 'Cybera Calgary')],
        'Cybera',
        'noc@cybera.ca',
        'sites-Cybera.conf')

    organization([
        (('bdw-dal.acorn-ns.ca', 'lat-dal.acorn-ns.ca'), 'Acorn Halifax'),
        (('198.165.161.195', None), 'Memorial Univ.')],
        'Acorn',
        'noc@acorn-ns.ca',
        'sites-Acorn.conf')

    organization([
        (('lat-sask1pfs1.srnet.ca', 'lat-sask1pfs1.srnet.ca'), 'SRnet Saskatchewan')],  # Only one node for both services
        'SRnet',
        'support@srnet.ca',
        'sites-SRnet.conf')

    organization([
        (('192.139.69.53', '192.139.69.53'), 'MRnet Winnipeg')],  # Only one node for both services
        'MRnet',
        'TODO',
        'sites-MRnet.conf')

    organization([
        (('bdw-gp-ftn.nbren.ca', 'lat-gp-ftn.nbren.ca'), 'Univ. of New Brunswick')],
        'REN',
        'TODO',
        'sites-REN.conf')

    organization([
        (('perfsonar.merlin.mb.ca', None), 'MERLIN Winnipeg')],
        'MERLIN',
        'TODO',
        'sites-MERLIN.conf')
