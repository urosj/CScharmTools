BASE_DIR=`pwd`
mkdir CScharm
cd CScharm
mkdir trusty
cd trusty
git clone https://github.com/CanonicalLtd/charmstore-charm.git
cd ..
juju deploy mongodb
juju deploy --repository . local:trusty/charmstore
juju expose charmstore
juju set charmstore source=v4
juju add-relation charmstore mongodb
cd $BASE_DIR