all: demo

demo: getproc
	./getproc $$$$

getproc: getproc.c
	gcc -save-temps $< -o $@


# remove builtin magics, for sane debug (-d) output
.SUFFIXES:
export MAKEFLAGS = --no-builtin-rules --no-builtin-variables
