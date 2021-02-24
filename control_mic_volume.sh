#!/bin/bash

# sudo alsamixer --> F6 --> snd_rpi_i2s_card --> F5 
arecord -D dmic_sv -c2 -r 44100 -f S32_LE -d 1 -t wav -V mono -v file.wav
amixer -c1 sset Boost 196
