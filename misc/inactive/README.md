# Deleting inactive devices

## my_network.htm
The page listing the known network devices; contains a value for pi and some other vars

eg

```
<meta name="pi" content="28Xt37r1077bM3N4">

<script language="JavaScript" type="text/javascript">
       var CGIs = ["myNetwork","owl"];
</script>

<script src="./nonAuth/globals.js"></script>
```

## apply.cgi
A call is made to apply.cgi from globals.js with these parameters


```
--data-binary 'CMD=&GO=my_network.htm&SET0=53813335%3Dd%252C7C%253AFF%253A48%253A70%253A8D%253A8A%253B&pi=IANp88wHLhou6PA3'

--data-binary 'CMD=&GO=my_network.htm&SET0= 53813335 %3D d%252C 7C %253A FF %253A 48 %253A 70 %253A 8D %253A 8A %253B &pi=IANp88wHLhou6PA3'

# setCfg("known_devices_update", "d," + devicesList_Iface[order].getMac(j) + ";");

# params = params + "&SET" + sub + "=" + String(CA[i].i) + "%3D"+ temp;

#  d%252C = d%2C = d,
#  %253A = %3A = :
#  %253B = %3B = ;
```
