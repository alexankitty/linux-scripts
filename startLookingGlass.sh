#!/bin/bash
virsh -c qemu:///system start win11
#looking-glass-client
#gamescope -W 2560 -H 1440 -b -f --cursor /home/alexandra/scripts/transparent.png --expose-wayland --force-grab-cursor -- looking-glass-client
__NV_DISABLE_EXPLICIT_SYNC=1 looking-glass-client
