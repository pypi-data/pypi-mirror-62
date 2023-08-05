# vim: set noexpandtab ts=4 sw=4:

# There must be a nicer way to do this
PYTHONARCH=$(shell python utils/pythonarch)
PYTHONARCH3=$(shell python3 utils/pythonarch)

BINS=$(shell python3 setup.py --list-scripts)

DEVELVERSION ?= 0.DEVEL.$(shell date +%Y%m%d%H%M)
RELEASEVERSION ?= $(DEVELVERSION)

all: $(PY4UICFILES)
	python3 setup.py build

all2: $(PY4UICFILES)
	python setup.py build

doc: doc-html

doc-html: all
	python3 setup.py build_sphinx

clean:
	python setup.py clean
	python3 setup.py clean
	# Stupid python setuptools don't even clean the build directory
	rm -fr build
	rm -fr doc/build

test3: all
	py.test-3 -c setup.cfg anamnesis

testv3: all
	py.test-3 -c setup.cfg -v anamnesis

test2: all2
	py.test -c setup.cfg anamnesis

testv2: all2
	py.test -c setup.cfg -v anamnesis

install:
	python3 setup.py install --prefix=$(DESTDIR)/usr
	mkdir -p $(DESTDIR)/usr/share/doc/anam
	cp -a doc/build/html $(DESTDIR)/usr/share/doc/anam

.PHONY: clean doc doc-html all all2 test3 testv3 test2 testv2 pythonarch
