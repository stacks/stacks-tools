#! /bin/bash

# url of Stacks project website
LOCALHOST="http://localhost:8080"
# location stacks-website directory relative to root webserver
# should start with a / if not empty
DIRECTORY=""
# absolute path to base directory to put website and tools
CURRENT=$(pwd)
# website will be placed in CURRENT/STACKSWEB
STACKSWEB="stacks-website"
# tools will be placed in CURRENT/STACKSTOOL
STACKSTOOL="stacks-tools"
# path to location of stacks project relative to CURRENT
# default choice is subdirectory 'tex' of website
PROJECTDIR=$STACKSWEB"/tex"
# directory in which to place database relative to STACKSWEB
# default choice is 'database'
DATABASEDIR="database"
# name database
DATABASENAME="stacks.sqlite"
# directory in which to place graph data
# default choice is subdirectory 'data' of website
# TODO This cannot be changed currently DONT CHANGE
DATADIR=$CURRENT"/"$STACKSWEB"/data"
# server from which to clone the stacks repositories
GITREPO="https://github.com/stacks/"

echo "This script tries to setup the Stacks project website locally"
echo
echo "Please check the values of the following variables: "
echo "LOCALHOST="$LOCALHOST
echo "DIRECTORY="$DIRECTORY
echo "CURRENT="$CURRENT
echo "STACKSWEB="$STACKSWEB
echo "STACKSTOOL="$STACKSTOOL
echo "PROJECTDIR="$PROJECTDIR
echo "DATABASEDIR="$DATABASEDIR
echo "DATABASENAME="$DATABASENAME
echo "DATADIR="$DATADIR
echo "GITREPO="$GITREPO
echo "Continue (y/n)"
read ANTWOORD
if [ ! $ANTWOORD = 'y' ]; then exit 0; fi

set -e

mkdir -p $CURRENT
cd $CURRENT

git clone ${GITREPO}stacks-website $STACKSWEB

cd $STACKSWEB

cat <<'EOF' > robots.txt
User-agent: *
Disallow: /
EOF

git submodule init

git submodule update

git clone ${GITREPO}stacks-project $CURRENT/$PROJECTDIR

cd $CURRENT/$PROJECTDIR

sed -i -e "s@http://stacks.math.columbia.edu/tag/@$LOCALHOST/tag/@" scripts/tag_up.py

make -j3 tags

cd $CURRENT

git clone ${GITREPO}stacks-tools $STACKSTOOL

cd $STACKSTOOL
sed -i -e "s@website =.*@website = \"../$STACKSWEB\"@" config.py
sed -i -e "s@database =.*@database = \"../$STACKSWEB/$DATABASEDIR/$DATABASENAME\"@" config.py
sed -i -e "s@websiteProject =.*@websiteProject = \"../$PROJECTDIR\"@" config.py

python create.py

mkdir $CURRENT/$STACKSWEB/$DATABASEDIR

chmod 0777 $CURRENT/$STACKSWEB/$DATABASEDIR

mv $CURRENT/$STACKSTOOL/stacks.sqlite $CURRENT/$STACKSWEB/$DATABASEDIR/$DATABASENAME

chmod 0777 $CURRENT/$STACKSWEB/$DATABASEDIR/$DATABASENAME

chmod 0777 $CURRENT/$STACKSWEB/php/cache

cd $CURRENT/$STACKSWEB
sed -i -e "s@database.*=.*@database = \"$DATABASEDIR/$DATABASENAME\"@" config.ini
sed -i -e "s@directory.*=.*@directory = \"$DIRECTORY\"@" config.ini
sed -i -e "s@project.*=.*@project = \"$CURRENT/$PROJECTDIR\"@" config.ini

ln -s ../../../../../css/stacks-editor.css js/EpicEditor/epiceditor/themes/editor/stacks-editor.css
ln -s ../../../../../css/stacks-preview.css js/EpicEditor/epiceditor/themes/preview/stacks-preview.css

sed -i -e "s@MathJax.Ajax.loadComplete(\"\[MathJax\]/extensions/TeX/xypic.js\");@MathJax.Ajax.loadComplete(\"/js/XyJax/extensions/TeX/xypic.js\");@" js/XyJax/extensions/TeX/xypic.js

sed -i -e "s@._SERVER\\[.*\\]@\"$CURRENT/$STACKSWEB\"@" php/config.php

cd $CURRENT/$STACKSTOOL

python update.py

python macros.py

cd $CURRENT

mkdir $DATADIR

cd $STACKSTOOL

python graphs.py
