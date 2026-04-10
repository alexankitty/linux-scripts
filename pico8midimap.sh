#!/usr/bin/env bash
declare -A map=(
  ["48"]=44
  ["49"]=31
  ["50"]=45
  ["51"]=32
  ["52"]=46
  ["53"]=47
  ["54"]=34
  ["55"]=48
  ["56"]=35
  ["57"]=49
  ["58"]=36
  ["59"]=50
  ["60"]=16
  ["61"]=3
  ["62"]=17
  ["63"]=4
  ["64"]=18
  ["65"]=19
  ["66"]=6
  ["67"]=20
  ["68"]=7
  ["69"]=21
  ["70"]=8
  ["71"]=22
  ["72"]=23
  ["73"]=10
  ["74"]=24
  ["75"]=11
  ["76"]=25
)

press_key(){
  midi_key=$1
  kb_key=${map["$1"]}
  case "$2" in
    "on") state=1;;
    "off") state=0;;
  esac
  if [ -z "$kb_key" ]; then
      return
  fi
  ydotool key "$kb_key:$state"
}

aseqdump -p 128:0 |
  while IFS=" ," read src ev1 ev2 ch label1 data1 label2 data2 rest; do
    if [ $ev1 = "Note" ]; then
      press_key $data1 $ev2
    fi
  done

