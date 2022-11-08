#!/bin/bash

sudo apt-get install wget

# remove older copy of file, if it exists
rm -f earthquakes.csv

# download latest data from USGS
wget https://github.com/devcmddef/meteorite/blob/main/mass_cor.csv
