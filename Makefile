.PHONY: test unicode2latex clean

test:
	make -C test

unicode2latex:
	make -C unicode2latex

clean:
	make -C test clean
	make -C unicode2latex clean

download:
	make -B jabbrv.sqlite

jabbrv.sqlite:
	time python3 download_jabbrv.py
