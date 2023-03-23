NASM= nasm -f elf
GCC= gcc
M32= -m32

converter.so: converter.o mul.o
	$(GCC) $(M32) converter.o -shared -o converter.so mul.o -lm
converter.o: converter.c macros.h
	$(GCC) -c $(M32) -fPIC converter.c -lm
mul.o: mul.asm 
	$(NASM) mul.asm
clean:
	rm *.o converter.so
