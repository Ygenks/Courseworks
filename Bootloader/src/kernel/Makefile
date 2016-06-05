all: startup.o main.o script.ld
	ld --oformat=binary -melf_i386 -T script.ld -o kernel.bin startup.o main.o
startup.o: startup.i386.asm
	fasm startup.i386.asm startup.o
main.o: main.c
	gcc -c -m32 -ffreestanding -o main.o main.c
clean:
	rm *.o kernel.bin 
