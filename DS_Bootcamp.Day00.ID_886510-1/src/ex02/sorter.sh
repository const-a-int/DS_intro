#!/bin/bash
{
    head -n 1 ../ex01/hh.csv
    tail -n +2 ../ex01/hh.csv | sort -t, -k2 -k1n 
} > hh_sorted.csv