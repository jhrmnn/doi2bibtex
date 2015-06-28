.PHONY: all test unicode2latex clean

dbname = jabbrv.db

all: unicode2latex $(dbname)

unicode2latex:
	$(MAKE) -C unicode2latex

test:
	$(MAKE) -C test

clean:
	$(MAKE) -C test clean
	$(MAKE) -C unicode2latex clean

download: download_jabbrv.py 
	-rm $(dbname)
	time python3 $<
	mv $(dbname) $(dbname).downloaded

$(dbname): process.sql
ifeq ("$(wildcard $(dbname).downloaded)", "")
	$(error "File $(dbname).downloaded missing. Run `make download`.")
endif
	cp $@.downloaded $@
	sqlite3 $@ <$(word 2, $^)
