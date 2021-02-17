#!/bin/bash
apt update
apt install fonts-unfonts-core -y
apt install ftp vim sox -y
apt install libhdf5-dev libatlas-base-dev libjasper-dev libqtgui4 libqt4-test -y
apt install tesseract-ocr tesseract-ocr-kor -y
apt install curl cmake openjdk-8-jdk -y
apt install --reinstall raspberrypi-bootloader raspberrypi-kernel -y

# Done
echo "DONE."
echo
echo "Settings take effect on next boot."
echo
echo -n "REBOOT NOW? [y/N] "
read
if [[ ! "$REPLY" =~ ^(yes|y|Y)$ ]]; then
        echo "Exiting without reboot."
        exit 0
fi
echo "Reboot started..."
reboot
exit 0

