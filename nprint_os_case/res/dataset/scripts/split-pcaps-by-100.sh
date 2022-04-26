#!/bin/bash
# NOTE : Quote it else use array to avoid problems #
FILES="../pcaps-100k/*"
for f in $FILES
do
  echo "Processing $f file..."
  echo ${f//pcaps-100k\//}
  editcap -c 100 $f "../pcaps-100/${f//..\/pcaps-100k\//}"
done