#! /bin/bash

LOCALHOST="http://localhost:8080"
DATABASEDIR="database/stacks.sqlite"
# The following starts with a / if not empty
DIRECTORY=""
PROJECTDIR=$(pwd)"/stacks-website/tex"

echo "Please check the values of the following variables: "
echo "LOCALHOST="$LOCALHOST
echo "DATABASEDIR="$DATABASEDIR
echo "DIRECTORY="$DIRECTORY
echo "PROJECTDIR="$PROJECTDIR
echo "Continue (y/n)"
read ANTWOORD
if [ ! $ANTWOORD = 'y' ]; then exit 0; fi


git clone https://github.com/stacks/stacks-website

cat <<'EOF' > stacks-website/robots.txt
User-agent: *
Disallow: /
EOF

cd stacks-website/

git submodule init

git submodule update

git clone git://github.com/stacks/stacks-project tex

sed -i -e "s@http://stacks.math.columbia.edu/tag/@$LOCALHOST/tag/@" tex/scripts/tag_up.py

cd tex

make -j3 tags

cd ../..

git clone https://github.com/stacks/stacks-tools

cd stacks-tools

python create.py

cd ..

mkdir stacks-website/database

chmod 0777 stacks-website/database

mv stacks-tools/stacks.sqlite stacks-website/database

chmod 0777 stacks-website/database/stacks.sqlite

chmod 0777 stacks-website/php/cache

sed -i -e "s@database.*=.*@database = \"$DATABASEDIR\"@" stacks-website/config.ini
sed -i -e "s@directory.*=.*@directory = \"$DIRECTORY\"@" stacks-website/config.ini
sed -i -e "s@project.*=.*@project = \"$PROJECTDIR\"@" stacks-website/config.ini

cd stacks-website

ln -s ../../../../../css/stacks-editor.css js/EpicEditor/epiceditor/themes/editor/stacks-editor.css
ln -s ../../../../../css/stacks-preview.css js/EpicEditor/epiceditor/themes/preview/stacks-preview.css

ln -s ../../../../js/XyJax/extensions/TeX/xypic.js js/MathJax/extensions/TeX/xypic.js
ln -s ../../../js/XyJax/extensions/fp.js js/MathJax/extensions/fp.js

cd ..

cd stacks-tools

python update.py

python macros.py

cd ..

mkdir stacks-website/data

cd stacks-tools

python graphs.py
