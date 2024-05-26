#!/bin/bash

ziperrorandexit() {
    echo make sure you have zip installed and you are in archlinux directory
    exit 1
}
main () {
    rm -rf build
    mkdir -p build
    cd ../..
    zip -r package/archlinux/build/namban-source.zip src || ziperrorandexit
    cd package
    zip -r archlinux/build/namban-source.zip files || ziperrorandexit
    cd archlinux || return
    cp PKGBUILD build
    cd build || return
    makepkg -sc
}

main