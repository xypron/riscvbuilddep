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

download http://de.archive.ubuntu.com/ubuntu/dists/lunar/main/source/Sources amd64/main/ Sources
download http://de.archive.ubuntu.com/ubuntu/dists/lunar/restricted/source/Sources amd64/restricted/ Sources
download http://de.archive.ubuntu.com/ubuntu/dists/lunar/universe/source/Sources amd64/universe/ Sources
download http://de.archive.ubuntu.com/ubuntu/dists/lunar/multiverse/source/Sources amd64/multiverse/ Sources
download http://de.archive.ubuntu.com/ubuntu/dists/lunar/main/binary-amd64/Packages amd64/main/ Packages
download http://de.archive.ubuntu.com/ubuntu/dists/lunar/restricted/binary-amd64/Packages amd64/resctricted/ Packages
download http://de.archive.ubuntu.com/ubuntu/dists/lunar/universe/binary-amd64/Packages amd64/universe/ Packages
download http://de.archive.ubuntu.com/ubuntu/dists/lunar/multiverse/binary-amd64/Packages amd64/multiverse/ Packages

download http://ports.ubuntu.com/ubuntu-ports/dists/lunar/main/source/Sources riscv64/main/ Sources
download http://ports.ubuntu.com/ubuntu-ports/dists/lunar/restricted/source/Sources riscv64/restricted/ Sources
download http://ports.ubuntu.com/ubuntu-ports/dists/lunar/universe/source/Sources riscv64/universe/ Sources
download http://ports.ubuntu.com/ubuntu-ports/dists/lunar/multiverse/source/Sources riscv64/multiverse/ Sources
download http://ports.ubuntu.com/ubuntu-ports/dists/lunar/main/binary-riscv64/Packages riscv64/main/ Packages
download http://ports.ubuntu.com/ubuntu-ports/dists/lunar/restricted/binary-riscv64/Packages riscv64/restricted Packages
download http://ports.ubuntu.com/ubuntu-ports/dists/lunar/universe/binary-riscv64/Packages riscv64/universe Packages
download http://ports.ubuntu.com/ubuntu-ports/dists/lunar/multiverse/binary-riscv64/Packages riscv64/multiverse Packages
