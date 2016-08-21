#! /bin/bash

#     _ _     _       
# ___| (_) __| |_   _ 
#/ __| | |/ _` | | | |
#\__ \ | | (_| | |_| |
#|___/_|_|\__,_|\__, |
#               |___/ 

rm -rf slidy
git clone https://github.com/slideshow-templates/slideshow-slidy.git slidy
rm -rf slidy/.git*



#                          _  _     
# _ __ _____   _____  __ _| |(_)___ 
#| '__/ _ \ \ / / _ \/ _` | || / __|
#| | |  __/\ V /  __/ (_| | || \__ \
#|_|  \___| \_/ \___|\__,_|_|/ |___/
#                          |__/     

rm -rf revealjs
git clone https://github.com/hakimel/reveal.js.git revealjs
rm -rf revealjs/.git*

#     _         _ _     _           
#  __| |_______| (_) __| | ___  ___ 
# / _` |_  / __| | |/ _` |/ _ \/ __|
#| (_| |/ /\__ \ | | (_| |  __/\__ \
# \__,_/___|___/_|_|\__,_|\___||___/
                                   
# the dzslides css is embedded in the html file directly unless --css is specified.
# we'll just get it

rm -rf dzslides
mkdir -p dzslides
echo "# Title" > trash.md
pandoc trash.md -o trash.html --standalone --to dzslides
sed -n "/\s*<style>/,/\s*<\/style>/ p" trash.html | head -n-1 | tail -n+2 > dzslides/dzslides.css
rm trash.md trash.html


#     _ _     _                      
# ___| (_) __| | ___  ___  _   _ ___ 
#/ __| | |/ _` |/ _ \/ _ \| | | / __|
#\__ \ | | (_| |  __/ (_) | |_| \__ \
#|___/_|_|\__,_|\___|\___/ \__,_|___/
                                    
rm -rf slideous
mkdir -p slidous
wget http://goessner.net/download/prj/slideous/slideous.zip
unzip slideous.zip -d slideous
rm slideous.zip
