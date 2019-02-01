.PHONY: all clean test

CSV := $(wildcard *.csv)
SUPA := $(patsubst %.csv,%.supa,$(CSV))

all: $(SUPA)

test:
	TEST=true ./rabo2supa.py

clean:
	rm $(SUPA) $(CSV)

%.supa: %.csv
	./rabo2supa.py $< > $@
