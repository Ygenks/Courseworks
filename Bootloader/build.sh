#!/bin/sh
make -C src
cp src/boot/boot.bios.bin bin/
cp src/kernel/kernel.bin bin/
cp src/make_listfs/make_listfs bin/

dd if=bin/boot.bios.bin of=bin/boot_sector.bin bs=512 count=1
dd if=bin/boot.bios.bin of=disk/boot.bin bs=1 skip=512
cp bin/kernel.bin disk/kernel.bin
bin/make_listfs of=disk.img bs=512 size=2880 boot=bin/boot_sector.bin src=./disk 

echo "Good work everyone!"
