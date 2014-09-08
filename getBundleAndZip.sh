BASE_DIR=`pwd`
mkdir tmpCharms
cd tmpCharms
TMP_CHARMS=`pwd`
cd $BASE_DIR
mkdir charmZips
cd charmZips
CHARM_ZIPS=`pwd`

#start downloading 
cd $TMP_CHARMS
mkdir $1
cd $1
bzr branch $2
cd bundle
mv bundles.yaml bundle.yaml
zip -r $CHARM_ZIPS/$1.zip .*

#remove temporary dir for charms
rm -rf $TMP_CHARMS
