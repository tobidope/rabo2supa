[![Build Status](https://travis-ci.org/tobidope/rabo2supa.svg?branch=master)](https://travis-ci.org/tobidope/rabo2supa)


rabo2supa.py converts https://www.rabodirect.de CSV account statements to the [SUPA format](http://www.subsembly.com/download/SUPA.pdf)
In this format they can be imported into the [banking4 suite](https://subsembly.com/banking4.html).

## Usage
Download the CSV into the checkout and type make
```shell-script
make
 ./rabo2supa.py Umsätze_20190201_DE94502102121002599538.csv > Umsätze_20190201_DE94502102121002599538.supa
 ```