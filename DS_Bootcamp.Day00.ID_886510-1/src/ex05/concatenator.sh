#!/bin/bash

head -n 1 2025-08-20.csv > hh_concatenated.csv

for file in $(ls *.csv | grep -v "hh_concatenated.csv"); do
    tail -n +2 "$file" >> hh_concatenated.csv
done