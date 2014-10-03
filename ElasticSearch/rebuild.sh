http delete localhost:9200/charmstore
http put localhost:9200/charmstore < index2.json
http put localhost:9200/charmstore/entity/_mapping < newentity.json
