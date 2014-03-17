#!/bin/bash
# This script convert ".config" file to ".json"

for file in $(find ./ -name '*.conf' | cut -c 3- | sort)
do
    # Append the .json extension instead of .config
    output=${file%%.*}.json
    /opt/perfsonar_ps/mesh_config/bin/build_json -input $file -output $output
    [ $? -ne 0 ] && echo Failure on file $file
done