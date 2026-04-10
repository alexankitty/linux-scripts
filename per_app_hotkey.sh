#!/usr/bin/env bash
running=($(pgrep -f "$0 $1"))
consumed=0

if [[ ${#running[@]} -ge 2 ]]; then
  exit
fi

active_window_class=$(hyprctl activewindow -j | jq -r ".class")

if [ "$active_window_class" = "$1" ]; then
  eval $2
  consumed=1
fi

if [ "$consumed" = 0 ]; then
  ydotool click --next-delay 1 0xc5
fi
