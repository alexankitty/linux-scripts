#!/usr/bin/env bash
num=$(shuf -i 0-999 -n 1)
if [[ $num -lt 10 ]]; then
  num="00${num}"
elif [[ $num -lt 100 ]]; then
  num="0${num}"
fi

passwd=$(xkcdpass -C capitalize -d '' -n 3 --min=3 --max=7)
echo "${passwd}${num}!"
