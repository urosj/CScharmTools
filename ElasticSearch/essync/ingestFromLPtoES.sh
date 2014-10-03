#!/bin/bash

# It is expected that: 
#	- mongo is already up and running.
# 	- Elasticsearch is up and running,
# 	- all on default ports,
#	- charmd, charmload and essync are in $GOPATH/bin 
#	- $GOPATH/bin is part of $PATH

charmd ./config.yaml &
charmload --logging-config="<root>=TRACE" --config="./config.yaml" --p=10
essync ./config.yaml