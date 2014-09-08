#!/bin/bash
# upload a charm, e.g.:
# upload-charm 10.0.0.1:8080 trusty/haproxy /home/frankban/devel/bundles/local/haproxy2.zip
# upload-charm 10.0.0.1.:8080 precise/memcached /home/frankban/devel/bundles/local/memc.zip

#md5=`/usr/bin/md5sum -b $3 | cut -d " " -f 1`
#sha=`/usr/bin/sha256sum -b $3 | cut -d " " -f 1`
sha=`shasum -a384 -b $3 | cut -d " " -f 1`

curl -ikL --data-binary @$3 \
    -H "Content-Type: application/zip" \
    http://bla:bla@$1/v4/$2/archive?hash=$sha
echo
