#! /bin/bash

# run the setup script in the origin directory if it exists.
origin="%ORIGIN%"

if [ -x $origin/setup.sh ]
then
  echo "Running setup.sh script in $origin."
  $origin/setup.sh
  exit 1
fi

src=$(dirname $0)

echo -n "Copying utilities..."
cp $src/HTMLSlideShowUtils ./ -r
cp $src/demo/slides.md ./ -r
cp $src/setup.sh ./
sed -i "/origin=/ s|%ORIGIN%|$src|" ./setup.sh
[ ! -h README.md ] && ln -s HTMLSlideShowUtils/README.md ./
[ ! -h Makefile ] && ln -s HTMLSlideShowUtils/Makefile ./
echo "done"

echo -n "Checking dependencies..."

if ! hash pandoc > /dev/null 2>&1
then
  echo "pandoc is required, but is not installed"
fi


missing_modules=$(HTMLSlideShowUtils/scripts/check-imports.py HTMLSlideShowUtils/scripts/* | grep -v 'macros')
if [ -n "${missing_modules}" ]
then
echo "These python modules are needed, but not installed"
echo "Please install them before building your presentation"
for module in ${missing_modules}
do
  echo "    ${module}"
done
fi
echo done
