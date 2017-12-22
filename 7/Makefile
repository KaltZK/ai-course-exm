all: build run
build:
	gcc -Wall -o main main.c state_helpers.c search.c
run:
	./main
battle:
	./main battle

win32: build_win32 run_win32	
build_win32:
	x86_64-w64-mingw32-gcc -Wall -o main.exe main.c state_helpers.c search.c
run_win32:
	WINEDEBUG=fixme-all wine main.exe