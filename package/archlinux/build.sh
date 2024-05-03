#!/bin/bash

ziperrorandexit() {
    echo make sure you have zip installed and you are in archlinux directory
    exit
}
main () {
    rm -rf build
    mkdir -p build
    cd ../..
    zip -r package/archlinux/build/namban-source.zip src systemd || ziperrorandexit
    cd package/archlinux || return
    cp PKGBUILD build
    cd build || return
    makepkg -sc
}

main