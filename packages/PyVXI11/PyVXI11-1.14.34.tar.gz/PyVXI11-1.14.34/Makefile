

all:clean cVXI11 vxi11scan vxi11_device_clear 

distclean:
	-rm cVXI11-*.{c,h,cpp}
	-rm cVXI11_*.{c,h,cpp}
	-rm VXI11_*.{c,h}
	-rm VXI11.h

cVXI11: setup.py
	python setup.py clean
	-python3 setup.py clean
	python setup.py build
	-python3 setup.py build

build: cVXI11


vxi11scan:vxi11_scan
	ln vxi11_scan vxi11scan

vxi11_scan:vxi11_scan.c VXI11_clnt.c  VXI11_xdr.c 
	$(CC) -g vxi11_scan.c VXI11_clnt.c  VXI11_xdr.c -o vxi11_scan

device_clear:vxi11_device_clear

vxi11_device_clear: misc/vxi11_device_clear.c VXI11_clnt.c  VXI11_xdr.c 
	$(CC) -g -I . misc/vxi11_device_clear.c VXI11_clnt.c  VXI11_xdr.c -o vxi11_device_clear

readme: README.rst
	/usr/local/bin/pandoc -t plain -o README README.rst
	/usr/local/bin/pandoc -t html -o README.html README.rst
	/usr/local/bin/pandoc -t markdown -o README.md README.rst

sdist:
	python3 setup.py sdist

upload: 
	python3 -m twine upload  dist/PyVXI11-1.14.31.tar.gz
