http delete localhost:9200/charmstore
http put localhost:9200/charmstore < index.json
http put localhost:9200/charmstore/entity/_mapping < entity.json
