# Deleting inactive devices

### /my_network.htm
The page listing the known network devices; contains a value for pi and some other vars

```
<meta name="pi" content="28Xt37r1077bM3N4">

<script language="JavaScript" type="text/javascript">
       var CGIs = ["myNetwork","owl"];
</script>

<script src="./nonAuth/globals.js"></script>
```
### /nonAuth/globals.js
```
// our CFG items use ";" as delimiter, it is not suitable for javascrip
// we need conver it to "%3B" from CFG_CGI routing if it is string conent
// also embedded inside CFG field.
// we also need conver to into "%3B" if want to setCfg().
// here use str2HTML() to conver to back, but some special operator like
// ":",".",",","-" can not be convert due to multi-fields CFG item use it
// as delimiter. ":" for MAC, "." for IP, "-" for range, "," for multi-range

function deleteDev(order, j, device){
...     
setCfg("known_devices_update", "d," + devicesList_Iface[order].getMac(j) + ";");
sendForm("my_network.htm", "", "");
...
}

function sendForm(cPage, _cmd, _waiting){
        var url ="/apply.cgi";
        xmlhttp.open("POST", url, true);
        var params = "CMD="+_cmd+ "&GO="+cPage;

        for (var i=0;i<CA.length;i++){
                if (CA[i].v!=CA[i].o){
                        temp = setCfg(CA[i].n, CA[i].v)
                        params = params + "&SET" + sub + "=" + String(CA[i].i) + "%3D"+ temp;
                        sub++;
                }
        }
```

### /apply.cgi

is passed the value of the cfg item known_devices_update, the "d," from deleteDev, the encoded MAC and the pi parameter eg:
```
'CMD=&GO=my_network.htm&SET0=53813335%3Dd%252C7C%253AFF%253A48%253A70%253A8D%253A8A%253B&pi=IANp88wHLhou6PA3'

CMD=&GO=my_network.htm&SET0= 53813335 %3D d%252C 7C %253A FF %253A 48 %253A 70 %253A 8D %253A 8A %253B 

 &pi=IANp88wHLhou6PA3'

#  #3D included in sendForm
#  53813335 = known_devices_update
#  d%252C = d%2C = d,
#  %253A = %3A = : ( MAC addr ) 
#  %253B = %3B = ; ( end of command? ) 
```
