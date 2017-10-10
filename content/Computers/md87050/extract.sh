#!/bin/bash

for PART in 1 2 3 4 5 6 7 8
do
    binwalk -M -e mtd$PART.img --directory mtd$PART.img.extracted
done

