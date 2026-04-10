#!/bin/bash

DEVICE="1-6.4"
DRIVER="/sys/bus/usb/drivers/snd-usb-audio"

#sleep 4

for i in 0 1 2; do
  echo "${DEVICE}:1.$i" >"${DRIVER}/unbind" 2>/dev/null
done
sleep 4
for i in 0 1 2; do
  echo "${DEVICE}:1.$i" >"${DRIVER}/bind" 2>/dev/null
done
