ffmpeg -f lavfi -i anullsrc=r=48000:cl=stereo -t 6 -f wav - |
  paplay --device=alsa_output.usb-YOWU_YOWU-4GS_20121120222026-00.analog-stereo
