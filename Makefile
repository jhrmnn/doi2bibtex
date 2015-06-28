.PHONY: all test unicode2latex sciabbr clean

all: unicode2latex sciabbr

unicode2latex:
	$(MAKE) -C unicode2latex

sciabbr:
	$(MAKE) -C sciabbr

test:
	$(MAKE) -C test

clean:
	$(MAKE) -C test clean
	$(MAKE) -C unicode2latex clean

