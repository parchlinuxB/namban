#!/bin/bash


pkgname="namban"
pkgver="0.3-1"
arch="amd64"
maintainer="meshya, D3F4U1T"
pkgdesc="A simple gui tool for set dns settings."
pkgdir="$(pwd)"/"$pkgname"_"$pkgver"_"$arch"
srcdir="$(pwd)/namban"

# TODO: Add the dependencies
# TODO: Create a CI/CD workflow to auto build the package

prepare() {
	git clone -b "v$pkgver" --depth=1 "https://github.com/parchlinuxB/namban"
}

package() {
	mkdir -p "$pkgdir/"{DEBIAN,'usr/'}
	cp -r "$srcdir/package/files/rootfs/"{usr,etc} "$pkgdir/"
	cp -r "$srcdir/src/" "$pkgdir/usr/lib/namban/src/"

	echo "Package: $pkgname
	Version: $pkgver
	Architecture: $arch
	Maintainer: $maintainer
	Description: $pkgdesc" | tr -d '\t' > "$pkgdir/DEBIAN/control"

	chmod +x "$pkgdir/usr/"{bin/namban,lib/namban/{nambanbin,namban-startup-check}}

	dpkg-deb --build --root-owner-group "$pkgdir"
}

cleanup() {
	rm -rf "$pkgdir"
	rm -rf "$srcdir"
}

prepare
package
cleanup
