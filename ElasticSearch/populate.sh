#/bin/bash

http put localhost:9200/charmstore/entity/anotherbundle < anotherbundle.json
http put localhost:9200/charmstore/entity/mwb < mediawiki-bundle.json
http put localhost:9200/charmstore/entity/mwc < mediawiki-charm.json
