dbname = abbrv.db

all:

download: download_abbrv.py 
	-rm $(dbname)
	time python3 $<
	mv $(dbname) $(dbname).downloaded

$(dbname): process.sql
ifeq ("$(wildcard $(dbname).downloaded)", "")
	$(error "File $(dbname).downloaded missing. Run `make download`.")
endif
	cp $@.downloaded $@
	sqlite3 $@ <$(word 2, $^)

