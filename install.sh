#!/bin/bash
sudo apt update
sudo apt install fonts-unfonts-core -y
sudo apt install ftp vim sox -y
sudo apt install libhdf5-dev libatlas-base-dev libjasper-dev libqtgui4 libqt4-test -y
sudo apt install tesseract-ocr tesseract-ocr-kor -y
sudo apt install curl openjdk-8-jdk -y
sudo pip3 install -r requirements.txt
bash <(curl -s https://raw.githubusercontent.com/konlpy/konlpy/master/scripts/mecab.sh)
wget https://project-downloads.drogon.net/wiringpi-latest.deb
sudo dpkg -i wiringpi-latest.deb
rm wiringpi-latest.deb
sudo systemctl disable hciuart.service
cd lib/servo;make;sudo make install;make clean
cd ../../utils/mic
./i2smic.sh
