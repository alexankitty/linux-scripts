#!/bin/sh
cd ~/git/Vesktop
git pull
pnpm i
pnpm package --linux pacman
sudo pacman -U ./dist/vesktop-*.pacman
rm ./dist/vesktop-*.pacman
