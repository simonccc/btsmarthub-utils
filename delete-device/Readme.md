# delete-device.py

Deletes a device from the smarthub interface ( useful for inactive devices )

## usage
```
./delete-device.py mac addr

./list-in-active.py  | sort -r  ( eg show oldest inactive devices )
```

## why?

I noticed when polling my smarthub for bandwidth usage a huge number of inactive devices.

These were typically transient vm's from my homelab with dynamicly generated mac addresses - so it was annoying to poll "dead" devices. And it meant the web interface was also slower / less responsive due to the size of the data the various js calls make.

See Notes.md for info I used working out how to make the request to delete a device
