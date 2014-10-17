sha=`shasum -a384 -b $3 | cut -d " " -f 1`

curl -ikL --data-binary @$3 \
    -H "Content-Type: application/zip" \
    http://admin:example-passwd@$1/v4/$2/archive?hash=$sha
echo
