# CS Charm Tools

## Usage


## Bundles
After the download process, open zip and edit bundle.yaml. In case the old name is bundles.yaml, rename it to bundle.yaml first. The first line should start with series. Then remove all 'cs:' prefixes in the names of the charms and also remove all the revision numbers. Note that in order to upload a bundle zip, all the charms should already be uploaded to the store. 

Using the processCharms.py with download flag, you can copy the mediabundlewiki.zip into a charmZips directory so that proper bundle.yaml is used.