for i in `./list-in-active.py  | grep "$1" | awk '{ print $5 }'`
do
  echo $i
  ./delete-device.py $i
done
