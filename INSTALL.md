* Directory 구조
<pre>
<code>
data/
example/ - 예제 파일
hw/ - MCU Firmware
lib/ - 라이브러리 모음
</code>
</pre>

* 사전설치
<pre>
<code>
sudo ./install.sh
</code>
</pre>

* 분야 별 참고사항
<pre>
<code>
# vision
sudo pip3 install opencv-python==4.1.0.25
sudo pip3 install opencv-contrib-python==4.1.0.25
sudo pip3 install dlib==19.19.0
sudo pip3 install pyzbar==0.1.8
sudo apt install libhdf5-dev libatlas-base-dev libjasper-dev libqtgui4 libqt4-test -y
sudo apt install tesseract-ocr-kor -y
 - 참고자료
  > object detection > (Caffe) mobileNet-SSD
  > ageGender detection > (Caffe) https://github.com/kairess/age_gender_estimation / https://github.com/GilLevi/AgeGenderDeepLearning

</code>
</pre>

<pre>
<code>
# konlpy
sudo apt install openjdk-8-jdk curl -y
sudo pip3 install konlpy
bash <(curl -s https://raw.githubusercontent.com/konlpy/konlpy/master/scripts/mecab.sh)

[참고] https://konlpy.org/
</code>
</pre>

<pre>
<code>
# 기타 설정 사항
- wifi 절전해제 : 해당 파일 없음
sudo vi /etc/modprobe.d/8192cu.conf
 edit "options 8192cu rtw_power_mgnt=0 rtw_enusbss=0"

 - wifi ssh 끊김문제 : US로 문제없어서 제거해도 될 듯
  wifi country GB로

  sudo vi /etc/modules : 기본으로 적재되어 있어 불필요
  추가 bcm2835-v4l2

 - Audio
   sudo raspi-config > System > Audio > 3.5mm

 - SPI 켜기
  [CLI]기준: sudo raspi-config > Interfacing Options > SPI 예
  [GUI]기준: 시작 > 기본설정 > Raspberry Pi Configuration > Interfaces > SPI Enable 

 - Raspberry Pi Configuration
  [CLI]기준: sudo raspi-config > Interfacing Options > Serial > login shell 아니오 , serial port 예
  [GUI]기준: 시작 > 기본설정 > Raspberry Pi Configuration > Interfaces > Serial Port Enable / Serial Console Disable

 - gitlab error(fatal: unable to access 'https://git.circul.us/leeyunjai/openpibo.git/': server certificate verification failed. CAfile: none CRLfile: none)
  git config --global http.sslverify false

 - sudo systemctl disable hciuart.service
</code>
</pre>

<pre>
<code>
# boot 관련 설정
- edit /etc/rc.local

 - Print the IP address
_IP=$(hostname -I) || true
if [ "$_IP" ]; then
  printf "My IP address is %s\n" "$_IP"
fi
/home/pi/openpibo/utils/boot/start.sh  <-- 추가
exit 0

</code>
</pre>

<pre>
<code>
# mic 설정
- .asoundrc
  local -> /home/pi/.asoundrc
  global -> /usr/share/alsa/alsa.conf
</code>
</pre>

<pre>
<code>
# splash 설정
#Raspberry Pi booting logo image changing 

sudo cp samplelogo.png /usr/share/plymouth/themes/pix/splash.png  
</code>
</pre>
