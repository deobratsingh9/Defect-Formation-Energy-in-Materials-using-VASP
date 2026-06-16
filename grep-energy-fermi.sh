#!/bin/bash

echo "# Folder TOTEN(eV) Fermi(eV)" > fe-data.dat

extract_data () {
local path=$1
TOTEN=$(grep "free  energy   TOTEN" "$path/OUTCAR" | tail -1 | awk '{print $5}')
FERMI=$(grep "E-fermi" "$path/OUTCAR" | tail -1 | awk '{print $3}')
echo "$path $TOTEN $FERMI" >> fe-data.dat
}

# First sic

[ -f "Bulk_SiC/OUTCAR" ] && extract_data "Bulk_SiC"

# Then c

[ -f "V_C/OUTCAR" ] && extract_data "V_C"

# Then c subfolders

if [ -d "V_C" ]; then
for subdir in V_C/*/; do
[ -f "${subdir}OUTCAR" ] || continue
extract_data "${subdir%/}"
done
fi

# Then all remaining folders

for dir in */; do
base=$(basename "$dir")
[ "$base" = "Bulk_SiC" ] && continue
[ "$base" = "V_C" ] && continue

```
[ -f "${dir}OUTCAR" ] && extract_data "${dir%/}"

for subdir in "${dir}"*/; do
    [ -d "$subdir" ] || continue
    [ -f "${subdir}OUTCAR" ] || continue
    extract_data "${subdir%/}"
done
```

done

cat fe-data.dat

