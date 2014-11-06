CC = gcc
OPT = -march=native -O3 -funroll-loops
CFLAGS = -Wall $(OPT) -fpic

all: lib

lib: libaft.so

libaft.so: eaf2d.o eaftest.o
	$(CC) -shared -o libaft.so eaf2d.o eaftest.o

eaf2d.o: eaf2d.c
	$(CC) $(CFLAGS) -o eaf2d.o -c eaf2d.c

eaftest.o: eaftest.c
	$(CC) $(CFLAGS) -DALLPOINTS -o eaftest.o -c eaftest.c

clean:
	$(RM) eaf2d.o eaftest.o

distclean: clean
	$(RM) libaft.so

