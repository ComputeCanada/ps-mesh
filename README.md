ps-mesh
=======

perfSonar Mesh configuration files

* sites-*region*.conf: Definition of local perfSonar nodes.
* sites-CC.conf: global mesh description
* tests-cc-latency.conf: definition of the full mesh latency tests for all CC sites.
* groups-*region*.conf: definition of mesh or disjoined groups.
* tests-*region*.conf: tests to run between group members.
* maddash.yaml: maddash server configuration (/etc/maddash/maddash-server/maddash.yaml).
* maddash-server-config.json: maddash server configuration (/opt/maddash/maddash-webui/etc/config.json).

Todo
====

* Change URL for http://ps-dashboard.computecanada.ca/ done
* Consortia to define *tests*, *groups* for their regions.
* Define inter-region bandwidth tests
* Add Canarie and ORANs perfSonar nodes for tests within region?
