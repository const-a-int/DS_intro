#!/bin/bash

INPUT="../ex03/hh_positions.csv"
OUTPUT="hh_uniq_positions.csv"

{
    echo '"name","count"'
    tail -n +2 "$INPUT" | awk -F, '$3 != "\"-\"" {print $3}' | sort | uniq -c | awk '{print $2 "," $1}' 
} > "$OUTPUT"
    
