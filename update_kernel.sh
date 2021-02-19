#!/bin/bash
wget https://archive.raspberrypi.org/debian/pool/main/r/raspberrypi-firmware/raspberrypi-kernel_1.20201126-1_armhf.deb
wget https://archive.raspberrypi.org/debian/pool/main/r/raspberrypi-firmware/raspberrypi-kernel-headers_1.20201126-1_armhf.deb
dpkg -i raspberrypi-kernel_1.20201126-1_armhf.deb
dpkg -i raspberrypi-kernel-headers_1.20201126-1_armhf.deb
sudo rfkill unblock wiki sudo rfkill unblock all

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

