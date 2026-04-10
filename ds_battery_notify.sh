#!/usr/bin/env bash

while true; do
  sleep 1
  battery=$(dualsensectl battery | cut -d ' ' -f 1)
  echo $battery
  if [[ $battery <= 10 ]]; then
    notify-send "Low Battery" "DualSense controller is at "
  fi
done
