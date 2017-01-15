# stdout off
# interactive off
bash
cd
cd tmp
rm -fr HTMLSlideShowUtils.tmp
mkdir HTMLSlideShowUtils.tmp
cd HTMLSlideShowUtils.tmp
export PS1="$ "
# interactive on
# stdout on
# pause 10

mkdir Code
# pause 10
cd Code
# pause 10
git clone https://github.com/CD3/HTMLSlideShowUtils
# pause 20
cd ..
# pause 10
mkdir Presentations
# pause 10
cd Presentations
# pause 10
../Code/HTMLSlideShowUtils/setup.sh
# pause 10
ls -l
# pause 10
make new-show NAME=Example
# pause 10
cd Example
# pause 10
cat slides.md
# pause 60
ls -l
# pause 10
make
# pause 30
ls -l
# pause 10
firefox html/00-slides.html
# pause 300
# interactive on
