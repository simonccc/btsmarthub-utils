# delete-device.py

Deletes a device from the smarthub interface ( useful for inactive devices )

## usage
```
./delete-device.py mac addr

./list-in-active.py  | sort -r  ( eg show oldest inactive devices )
```

## why?

I noticed when polling the smarthub for bandwidth usage a huge number of inactive devices.

These are typically vm's from my homelab but it was annoying to poll "dead" devices.

See Notes.md for info I used working out how to make the request to delete a device
