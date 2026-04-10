#!/bin/bash

DEVICE="1-6.4"
DRIVER="/sys/bus/usb/drivers/snd-usb-audio"

if [ -d "$DRIVER/$DEVICE:1.2" ]; then
    echo Unbinding headset.
    for i in 0 1 2; do
        echo "${DEVICE}:1.$i" >"${DRIVER}/unbind" 2>/dev/null
    done
else
    echo Binding headset.
    for i in 0 1 2; do
        echo "${DEVICE}:1.$i" >"${DRIVER}/bind" 2>/dev/null
    done
fi

