#!/bin/bash

# $1 is the name of original zip file, name.zip
# $2 is the name of revision copy, name-1.zip
# $3 is the name of a dir where it is extracted, name-1

cp ./charmZips/$1.zip ./charmRevisions/$1-$2.zip
cd ./charmRevisions
unzip $1-$2.zip -d $1-$2
rm -rf $1-$2.zip
cd $1-$2
echo $3 > revision
#zip -r ../$1-$2.zip .
cd ..
../zipper zip $1-$2 > $1-$2.zip
rm -rf $1-$2
