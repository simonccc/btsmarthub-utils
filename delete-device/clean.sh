read foo
echo cleaning $foo
for i in `./list-in-active.py | grep ${foo} | awk '{ print $5 }'`
do
echo $i
./delete-device.py $i
done
