#!/bin/bash
pip3 install -r requirements.txt
bash <(curl -s https://raw.githubusercontent.com/konlpy/konlpy/master/scripts/mecab.sh)
wget https://project-downloads.drogon.net/wiringpi-latest.deb
dpkg -i wiringpi-latest.deb
rm wiringpi-latest.deb
systemctl disable hciuart.service
cd lib/servo;make;sudo make install;make clean
cd ../../utils/mic
./i2smic.sh
