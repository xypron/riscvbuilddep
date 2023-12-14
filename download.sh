#!/bin/sh

set -e

# download() - download a text file
#
# $1 -- filename to download without '.gz' extension
# $2 -- installation path
# $3 -- installation file name
#
download()
{
	rm -f .tmp .tmp.gz
	wget "$1.gz" -O .tmp.gz
	gzip -d .tmp.gz
	mkdir -p $2
	mv .tmp "$2/$3"
}

download http://de.archive.ubuntu.com/ubuntu/dists/noble/main/source/Sources amd64/main/ Sources
download http://de.archive.ubuntu.com/ubuntu/dists/noble/restricted/source/Sources amd64/restricted/ Sources
download http://de.archive.ubuntu.com/ubuntu/dists/noble/universe/source/Sources amd64/universe/ Sources
download http://de.archive.ubuntu.com/ubuntu/dists/noble/multiverse/source/Sources amd64/multiverse/ Sources
download http://de.archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages amd64/main/ Packages
download http://de.archive.ubuntu.com/ubuntu/dists/noble/restricted/binary-amd64/Packages amd64/resctricted/ Packages
download http://de.archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages amd64/universe/ Packages
download http://de.archive.ubuntu.com/ubuntu/dists/noble/multiverse/binary-amd64/Packages amd64/multiverse/ Packages

download http://ports.ubuntu.com/ubuntu-ports/dists/noble/main/source/Sources riscv64/main/ Sources
download http://ports.ubuntu.com/ubuntu-ports/dists/noble/restricted/source/Sources riscv64/restricted/ Sources
download http://ports.ubuntu.com/ubuntu-ports/dists/noble/universe/source/Sources riscv64/universe/ Sources
download http://ports.ubuntu.com/ubuntu-ports/dists/noble/multiverse/source/Sources riscv64/multiverse/ Sources
download http://ports.ubuntu.com/ubuntu-ports/dists/noble/main/binary-riscv64/Packages riscv64/main/ Packages
download http://ports.ubuntu.com/ubuntu-ports/dists/noble/restricted/binary-riscv64/Packages riscv64/restricted Packages
download http://ports.ubuntu.com/ubuntu-ports/dists/noble/universe/binary-riscv64/Packages riscv64/universe Packages
download http://ports.ubuntu.com/ubuntu-ports/dists/noble/multiverse/binary-riscv64/Packages riscv64/multiverse Packages

download http://ports.ubuntu.com/ubuntu-ports/dists/noble/main/source/Sources arm64/main/ Sources
download http://ports.ubuntu.com/ubuntu-ports/dists/noble/restricted/source/Sources arm64/restricted/ Sources
download http://ports.ubuntu.com/ubuntu-ports/dists/noble/universe/source/Sources arm64/universe/ Sources
download http://ports.ubuntu.com/ubuntu-ports/dists/noble/multiverse/source/Sources arm64/multiverse/ Sources
download http://ports.ubuntu.com/ubuntu-ports/dists/noble/main/binary-arm64/Packages arm64/main/ Packages
download http://ports.ubuntu.com/ubuntu-ports/dists/noble/restricted/binary-arm64/Packages arm64/restricted Packages
download http://ports.ubuntu.com/ubuntu-ports/dists/noble/universe/binary-arm64/Packages arm64/universe Packages
download http://ports.ubuntu.com/ubuntu-ports/dists/noble/multiverse/binary-arm64/Packages arm64/multiverse Packages
