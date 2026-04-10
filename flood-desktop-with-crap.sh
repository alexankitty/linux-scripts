#! /usr/bin/env bash

limit=200

randomexts=("jpg" "png" "pdf" "docx" "xlsx" "pptx" "txt" "csv" "zip" "tar.gz" "mp3" "mp4" "avi" "mkv" "flac" "wav" "ogg" "exe" "dll" "iso" "apk" "deb" "rpm" "bin" "sh" "py" "js" "html" "css" "json" "xml" "yml" "md" "log" "bak" "tmp" "cfg" "ini" "conf" "env" "key" "pem" "crt" "csr" "pfx" "p12" "cer" "der" "csr" "key" "pem" "pfx" "p12" "cer" "der")
extcount=$((${#randomexts[@]}))

increment=0
while true; do
    increment=$((increment + 1))
    randomwords=$(xkcdpass -n 3 -d '')
    randomext=${randomexts[$((RANDOM % extcount))]}
    touch "$HOME/Desktop/${randomwords}.${randomext}"
    echo "Created file: $HOME/Desktop/${randomwords}.${randomext}"
    if [ $increment -ge $limit ]; then
        break
    fi
done