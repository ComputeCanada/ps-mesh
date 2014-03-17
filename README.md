ps-mesh
=======

perfSonar Mesh configuration files

* sites-*region*.conf: Definition of local persSonar nodes.
* sites-CC.conf: global mesh description
* tests-cc-allsites.conf: definition of the tests. Includes the full
  mesh latency test, full mesh bandwidth within a region.

Todo
====

* Change URL for http://ps-dashboard.computecanada.ca/ ?
* Uncomment *tests*, *groups* and *members* in tests-cc-allsites.conf when the
  corresponding sites-*region*.conf files are available.
* Define inter-region bandwidth tests
* Add Canarie perfSonar nodes for tests within region?
