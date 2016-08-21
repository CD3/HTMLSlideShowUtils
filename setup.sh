#! /bin/bash

dir=$(dirname $0)

echo -n "Copying utilities..."
cp $dir/HTMLSlideShowUtils ./ -r
cp $dir/demo/slides.md ./ -r
ln -s HTMLSlideShowUtils/README.md ./
ln -s HTMLSlideShowUtils/Makefile ./
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
