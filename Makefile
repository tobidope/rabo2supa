.PHONY: all clean test

CSV := $(wildcard *.csv)
SUPA := $(patsubst %.csv,%.supa,$(CSV))

all: $(SUPA)

test:
	pytest

clean:
	rm $(SUPA) $(CSV)

%.supa: %.csv
	./rabo2supa.py $< > $@
