#!/bin/bash
#Uploads selected charms from the charmsDir location.
#The only paramer required is an IP and port of the charmstore.
#
#example:
#./uploadCharms 10.0.0.1:8080 

echo "uploading apache2"
./upload-charm.sh $1 precise/apache2 charmZips/apache2.zip
echo "uploading cassandra"
./upload-charm.sh $1 precise/cassandra charmZips/cassandra.zip
echo "uploading drupal6"
./upload-charm.sh $1 precise/drupal6 charmZips/drupal6.zip
echo "uploading elastic search"
./upload-charm.sh $1 precise/elasticsearch charmZips/elasticsearch.zip
echo "uploading juju-gui"
./upload-charm.sh $1 precise/juju-gui charmZips/jujugui.zip
echo "uploading memcached"
./upload-charm.sh $1 precise/memcached charmZips/memcached.zip
echo "uploading rabbitmq-server"
./upload-charm.sh $1 precise/rabbitmqserver charmZips/rabbitmqserver.zip
echo "uploading solr"
./upload-charm.sh $1 precise/solr charmZips/solr.zip
echo "uploading tomcat7"
./upload-charm.sh $1 precise/tomcat7 charmZips/tomcat7.zip
echo "uploading wordpress"
./upload-charm.sh $1 precise/wordpress charmZips/wordpress.zip
echo "uploading zookeeper"
./upload-charm.sh $1 precise/zookeeper charmZips/zookeeper.zip
