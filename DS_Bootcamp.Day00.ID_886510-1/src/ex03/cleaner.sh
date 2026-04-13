#!/bin/bash

OUTPUT="hh_positions.csv"
INPUT="../ex02/hh_sorted.csv"

head -n 1 ../ex01/hh.csv > "$OUTPUT"

awk -F, '
    NR == 1 {next}
    {
        level="-"
        if ($3 ~ /Junior/) level = "Junior" 
        if ($3 ~ /Middle/) level = "Middle"
        if ($3 ~ /Senior/) level = "Senior" 
        print $1 "," $2 "," "\"" level "\"" "," $4 "," $5  
    }
' "$INPUT"  >> "$OUTPUT"
    