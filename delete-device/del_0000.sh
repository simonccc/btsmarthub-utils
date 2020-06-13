
for i in `./list-in-active.py  | grep 0.0.0.0 | awk '{ print $5 }'`
do
  echo $i
  ./delete-device.py $i
done
