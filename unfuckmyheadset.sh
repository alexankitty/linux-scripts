s=5
timeout=0.2
x=0
y="$(echo "$s / $timeout" | bc -l)"
y=${y%.*}
while [ $x -lt $y ]; do
  pactl suspend-sink alsa_output.usb-YOWU_YOWU-4GS_20121120222026-00.analog-stereo true
  sleep $timeout
  x=$((x + 1))
done
