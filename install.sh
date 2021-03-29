#!/bin/bash
wget https://archive.raspberrypi.org/debian/pool/main/r/raspberrypi-firmware/raspberrypi-kernel-headers_1.20201126-1_armhf.deb
dpkg -i raspberrypi-kernel-headers_1.20201126-1_armhf.deb
rm -f raspberrypi-kernel-headers_1.20201126-1_armhf.deb

#sudo rfkill unblock wiki sudo rfkill unblock all

apt update
apt install fonts-unfonts-core -y
apt install ftp vim sox -y
apt install python3-dev python3-pip -y
apt install libhdf5-dev libatlas-base-dev libjasper-dev libqtgui4 libqt4-test -y
apt install tesseract-ocr tesseract-ocr-kor -y
apt install curl cmake openjdk-8-jdk -y
apt install omxplayer -y
apt install libilmbase23 libopenexr-dev libswscale-dev libzbar0 -y
#apt install --reinstall raspberrypi-bootloader raspberrypi-kernel -y

pip3 install -r requirements.txt
bash <(curl -s https://raw.githubusercontent.com/konlpy/konlpy/master/scripts/mecab.sh)
wget https://project-downloads.drogon.net/wiringpi-latest.deb
dpkg -i wiringpi-latest.deb
rm wiringpi-latest.deb
systemctl disable hciuart.service
cd lib/servo;make;sudo make install;make clean
cd ../../utils/mic
./i2smic.sh