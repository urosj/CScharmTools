#!/bin/bash
#bzr must be installed before running the script
BASE_DIR=`pwd`
mkdir tmpCharms
cd tmpCharms
TMP_CHARMS=`pwd`
cd $BASE_DIR
mkdir charmZips
cd charmZips
CHARM_ZIPS=`pwd`

#start downloading 
#Apache2
cd $TMP_CHARMS
mkdir apache2
cd apache2
bzr branch lp:~charmers/charms/precise/apache2/trunk
cd trunk
zip -r $CHARM_ZIPS/apache2.zip .*

#cassandra
cd $TMP_CHARMS
mkdir cassandra
cd cassandra
bzr branch lp:~charmers/charms/precise/cassandra/trunk
cd trunk
zip -r $CHARM_ZIPS/cassandra.zip .*

#elasticsearch
cd $TMP_CHARMS
mkdir elasticsearch
cd elasticsearch
bzr branch lp:~charmers/charms/precise/elasticsearch/trunk
cd trunk
zip -r $CHARM_ZIPS/elasticsearch.zip .*

#drupal6
cd $TMP_CHARMS
mkdir drupal6
cd drupal6
bzr branch lp:~lynxman/charms/precise/drupal6/trunk
cd trunk
zip -r $CHARM_ZIPS/drupal6.zip .*

#jujugui
cd $TMP_CHARMS
mkdir jujugui
cd jujugui
bzr branch lp:~juju-gui-charmers/charms/precise/juju-gui/trunk
cd trunk
zip -r $CHARM_ZIPS/jujugui.zip .*

#memcached
cd $TMP_CHARMS
mkdir memcached
cd memcached
bzr branch lp:~charmers/charms/precise/memcached/trunk
cd trunk
zip -r $CHARM_ZIPS/memcached.zip .*

#rabbitmqserver
cd $TMP_CHARMS
mkdir rabbitmqserver
cd rabbitmqserver
bzr branch lp:~charmers/charms/precise/rabbitmq-server/trunk
cd trunk
zip -r $CHARM_ZIPS/rabbitmqserver.zip .*

#solr
cd $TMP_CHARMS
mkdir solr
cd solr
bzr branch lp:~charmers/charms/precise/solr/trunk
cd trunk
zip -r $CHARM_ZIPS/solr.zip .*

#tomcat7
cd $TMP_CHARMS
mkdir tomcat7
cd tomcat7
bzr branch lp:~charmers/charms/precise/tomcat7/trunk
cd trunk
zip -r $CHARM_ZIPS/tomcat7.zip .*

#wordpress
cd $TMP_CHARMS
mkdir wordpress
cd wordpress
bzr branch lp:~charmers/charms/precise/wordpress/trunk
cd trunk
zip -r $CHARM_ZIPS/wordpress.zip .*

#zookeeper
cd $TMP_CHARMS
mkdir zookeeper
cd zookeeper
bzr branch lp:~charmers/charms/precise/zookeeper/trunk
cd trunk
zip -r $CHARM_ZIPS/zookeeper.zip .*

#remove temporary dir for charms
rm -rf $TMP_CHARMS
