#!/bin/bash

INPUT="../ex03/hh_positions.csv"

tail -n +2 "$INPUT" | while IFS= read -r line; do
    date=$(echo "$line" | awk -F, '{print $2}' | cut -c 2-11)
    output_file="${date}.csv"
    if [ ! -f "$output_file" ]; 
        then head -n 1 "$INPUT" > "$output_file"
    fi
        echo "$line" >> "$output_file"
done