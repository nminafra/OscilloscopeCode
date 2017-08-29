#BOOST_INCLUDE="/afs/cern.ch/user/n/nminafra/Work/public/boost/"
ROOT=`root-config --cflags --libs`

INS=-Iinclude #$(BOOST_INCLUDE)
CC=g++
CFLAGS=-O3 -Wall -DNUM_DOUBLE -std=c++11
SOFLAGS=-fPIC

all:Oscilloscope_readData.a oscilloscope_readData

src/Oscilloscope_readData.o: src/Oscilloscope_readData.cxx include/Oscilloscope_readData.h
	$(CC) $(SOFLAGS) $(CFLAGS) -c -o $@ $< $(ROOT) $(INS)

objects=Oscilloscope_readData.o 
f_0_objects=$(objects:%=src/%)

Oscilloscope_readData.a:$(f_0_objects)
	ar -r $@ $(f_0_objects)

oscilloscope_readData:%:%.cxx Oscilloscope_readData.a
	g++ -o $@ $< -Iinclude  Oscilloscope_readData.a $(ROOT)

.cxx.o:
	$(CC) $(CFLAGS) $(SOFLAGS) $(INS) -c $< -o $@ $< $(ROOT)

clean:
	rm -f *.a src/*.o oscilloscope_readData AutoDict*



