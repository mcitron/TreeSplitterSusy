SOURCES=cutTree.cpp
OBJECTS=$(SOURCES:.cpp=.o)
EXECUTABLE=cutTreeSusy

CC      = g++
CCFLAG = -g -c -Wall  $(shell root-config --cflags)
LDFLAG = $(shell root-config --libs) -L/usr/local/root/lib -lGenVector

$(EXECUTABLE): $(OBJECTS)
	$(CC) -o $@ $^ $(LDFLAG)

.cpp.o:
	$(CC) -I. $(CCFLAG) -o $@ $<

all: $(SOURCES) $(EXECUTABLE) 

clean:
	rm -f *.o *.so
	rm -f cutTreeSusy
