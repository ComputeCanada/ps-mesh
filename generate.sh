#!/bin/bash
# This script convert ".conf" files to a single ".json"

./scraper.py

cat ComputeCanada.conf > all.conf
cat sites*.conf >> all.conf
cat tests*.conf >> all.conf
/opt/perfsonar_ps/mesh_config/bin/build_json -input all.conf -output all.json
