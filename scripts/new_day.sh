#!/bin/bash

last_created=$(find . -name "D*" -type d | cut -dD -f2 | sort -n | tail -1)

echo "Last created day: $last_created"

# get the day of the month
d=$(date +%d)
m=$(date +%m)
y=$(date +%Y)

echo "Today is day $d/$m/$y"

if [ "$last_created" -lt "$d" ]; then
    echo "Creating day $d"
    mkdir "D$d"
    sed "s/@DAY@/$d/g" < "scripts/code_template.py" > "D$d/code.py"
    touch "D$d/input.txt"
    touch "D$d/__init__.py"
    git add "D$d"
    exit 0
fi

if [ "$last_created" -eq "$d" ]; then
    echo "We're up to date... Be patient!!"
    exit 0
fi

