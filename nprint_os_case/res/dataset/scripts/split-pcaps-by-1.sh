#!/bin/bash
# NOTE : Quote it else use array to avoid problems #
FILES="../pcaps-ip/*"
for f in $FILES
do
  echo "Processing $f file..."
  echo ${f//..\/pcaps-ip\//}
  editcap -c 1 $f "../pcaps/${f//..\/pcaps-ip\//}"
done