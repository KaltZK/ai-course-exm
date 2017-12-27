all: build run
build:
	g++ -Wall -o main main.cpp state.cpp
run:
	./main
battle:
	./main battle

win32: build_win32 run_win32
build_win32:
	i686-w64-mingw32-g++ -Wall -o main.exe main.cpp state.cpp
run_win32:
	WINEDEBUG=fixme-all wine main.exe