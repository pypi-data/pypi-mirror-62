CFLAGS := -Wall -O0 -ggdb -std=c11

all: init stub cythonize build sdist bdist_wheel

init:
	pip install -Ur dev-requirements.txt
	touch init

cythonize:
	cythonize mock.pyx -3 --build

stub:
	stubgen mock.pyx
	mv out/__main__.pyi mock.pyi

build:
	python setup.py build

sdist:
	python setup.py sdist

bdist_wheel:
	python setup.py bdist_wheel

clean:
	$(RM) mock.cpython* -v
	$(RM) mock.c -v
	$(RM) mock.pyi -v
	$(RM) dist -Rv
	$(RM) cymock.egg-info -Rv 
	$(RM) build -Rv

.PHONY: all stub cythonize build sdist bdist_wheel clean
