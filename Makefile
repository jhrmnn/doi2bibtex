.PHONY: all test unicode2latex sciabbr clean

all: unicode2latex

unicode2latex:
	$(MAKE) -C unicode2latex

test:
	$(MAKE) -C test

clean:
	$(MAKE) -C test clean
	$(MAKE) -C unicode2latex clean

