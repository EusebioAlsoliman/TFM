INC_DIR = /home/eusebio/EPICS/epics-base/include
INC_DIR = /home/eusebio/EPICS/epics-base/lib/liblinux-x86_64/

#DEPS = $(INC_DIR)

#CFLAGS  = -c -Wall -Iinclude

VPATH = /home/eusebio/EPICS/epics-base/include
VPATH = /home/eusebio/EPICS/epics-base/lib/liblinux-x86_64/

CC=g++

# This is the default target, which will be built when 
# you invoke make
.PHONY: all
all: hello

# This rule tells make how to build hello from hello.cpp
hello: hello.cpp
# $(CC) -D_GNU_SOURCE -D_DEFAULT_SOURCE -D_X86_64_  -DUNIX  -Dlinux -O3 -g   -Wall     -std=c++11  -mtune=generic -m64 -I/home/eusebio/EPICS/epics-base/include -I/home/eusebio/EPICS/epics-base/include/lib -I/home/eusebio/EPICS/epics-base/include/compiler/gcc -I/home/eusebio/EPICS/epics-base/ -L/home/eusebio/EPICS/epics-base/lib/linux-x86_64 -lpvAccess -lpvData hello.cpp -o hello
	$(CC) -D_GNU_SOURCE -mtune=generic -I/home/eusebio/EPICS/epics-base -I/home/eusebio/EPICS/epics-base/include -I/home/eusebio/EPICS/epics-base/include/os/Linux -I/home/eusebio/EPICS/epics-base/include/lib -I/home/eusebio/EPICS/epics-base/include/compiler/gcc -I/home/eusebio/EPICS/epics-base/ -L/home/eusebio/EPICS/epics-base/lib/linux-x86_64 -lpvAccess -lpvData -lCom -lpvAccessCA -lpvAccessIOC -lpvaClient hello.cpp -o hello
# -I /home/eusebio/EPICS/epics-base/liblinux-x86_64/
# $(CC) -c $< -o $@
#	hello: $(DEPS)

# This rule tells make to copy hello to the binaries subdirectory,
# creating it if necessary
.PHONY: install
install:
	mkdir -p binaries
	cp -p hello binaries

# This rule tells make to delete hello and hello.o
.PHONY: clean 
clean:
	rm -f hello

# g++  -D_GNU_SOURCE -D_DEFAULT_SOURCE           -D_X86_64_  -DUNIX  -Dlinux     -O3 -g   -Wall     -std=c++11  -mtune=generic     -m64  -I. -I../O.Common -I. -I. -I.. -I../../../include/compiler/gcc -I../../../include/os/Linux -I../../../include -I/home/martins/epics/base/include/compiler/gcc -I/home/martins/epics/base/include/os/Linux -I/home/martins/epics/base/include        -c ../main.cpp
# g++ -o test  -L/home/martins/test-clientprovider/lib/linux-x86_64 -L/home/martins/epics/epics-base/lib/linux-x86_64 -Wl,-rpath,/home/martins/test-clientprovider/lib/linux-x86_64 -Wl,-rpath,/home/martins/epics/epics-base/lib/linux-x86_64           -rdynamic -m64            main.o    -lpvAccess -lpvData   
