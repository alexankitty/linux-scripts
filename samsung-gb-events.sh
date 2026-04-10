#! /bin/env bash
device='/dev/input/by-path/platform-SAM0430:00-event'

key_perf='*type 1 (EV_KEY), code 202 (KEY_PROG3), value 1*'

evtest "$device" | while read line; do
  perf_mode=$(cat /sys/firmware/acpi/platform_profile)
  perf_mode=(${perf_mode//-/ })
  perf_mode=${perf_mode[@]^}
  case $line in
  $key_perf) notify-send "Power" "Power mode changed to $perf_mode." ;;
  esac
done
