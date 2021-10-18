#!/bin/bash
# NOTE : Quote it else use array to avoid problems #
FILES="pcaps-ip/*"
for f in $FILES
do
  echo "Processing $f file..."
  echo ${f//pcaps-ip\//}
  editcap -r $f "pcaps-100k/100k-${f//pcaps-ip\//}" 1-100000
done