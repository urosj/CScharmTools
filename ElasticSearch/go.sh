#!/bin/bash

set -eux

# :9200 implies localhost:9200
http DELETE :9200/charmstore/

http PUT :9200/charmstore < index2.json

http PUT :9200/charmstore/entity/_mapping < entity.json

http GET :9200/charmstore/_settings

http POST :9200/charmstore/entity/mw < mediawiki-charm.json

# An example of ngram searching. Note the quotes are required.
#http GET ":9200/charmstore/entity/_search" < search_ngram.json
