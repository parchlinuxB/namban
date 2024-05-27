#!/bin/bash
checkrequieremnts(){
    if type rsvg-convert > /dev/null 2>&1; then
        return 
    else
        echo "Install librsvg and try again"
        echo "If librsvg already is installed make sure that rsvg-convert command works"
        exit 1
    fi
}

buildIcon(){
    mkdir -p rootfs/usr/share/icons/hicolor/$1x$1/apps
    rsvg-convert -w $1 -h $1 -o rootfs/usr/share/icons/hicolor/$1x$1/apps/namban.png ../../namban.svg
}
main (){
    checkrequieremnts
    buildIcon 16
    buildIcon 22
    buildIcon 24
    buildIcon 32
    buildIcon 48
    mkdir -p rootfs/usr/share/icons/hicolor/scalable/apps
    cp ../../namban.svg rootfs/usr/share/icons/hicolor/scalable/apps/namban.svg
    echo "Building icons finished successfuly"
}
main