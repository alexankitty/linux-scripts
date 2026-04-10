#!/bin/bash
# /usr/local/bin/yowu-fix.sh
SINK="alsa_output.usb-YOWU_YOWU-4GS_20121120222026-00.analog-stereo"

# Wait for sink to actually exist
for i in $(seq 1 30); do
  pactl list sinks short | grep -q "$SINK" && break
  sleep 0.5
done

# Now do the suspend cycle to let RF link settle
sleep 2
pactl suspend-sink "$SINK" true
sleep 0.5
pactl suspend-sink "$SINK" false
