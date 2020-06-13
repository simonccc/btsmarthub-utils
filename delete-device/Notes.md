# Deleting inactive devices

Notes on how this works... functions and code below simplfied for clarity

1. login / get cookie
2. get pi
3. get the known_devices_update variable/number by calling cgi_myNetwork.js with the current timestamp
4. generate the post to apply.cgi with the known_devices_update id, the encoded MAC and pi value per the formats specified in deleteDevice and sendForm

More info: 

### /my_network.htm
page listing the known network devices, the vars for pi and CGI's to be called to generate the page content

```
<meta name="pi" content="28Xt37r1077bM3N4">
var CGIs = ["myNetwork","owl"];
```

### /nonAuth/globals.js
is called by /my_network.htm and provides a bunch of functions

#### pi
seems to be the identifier linking a unique set of cfg ids - when pi is renewed the CGI's are called again.
```
function renew_CGI_pi()
  change_pi_var = new HTTP_Request(change_pi);
  change_pi_var.request("cgi/renewPi.js", "GET");
	  for(var i=0; i < CGIs.length;i++){
		  k="cgi/cgi_"+CGIs[i]+'.js?t='+ Date.now()
```

#### URL encoding
there is some kind of double encoding going on
```
// our CFG items use ";" as delimiter, it is not suitable for javascrip
// we need conver it to "%3B" from CFG_CGI routing if it is string conent
// also embedded inside CFG field.
// we also need conver to into "%3B" if want to setCfg().
// here use str2HTML() to conver to back, but some special operator like
// ":",".",",","-" can not be convert due to multi-fields CFG item use it
// as delimiter. ":" for MAC, "." for IP, "-" for range, "," for multi-range
```

#### deleteDev

this gives us the parameters to the apply.cgi POST later on
```
function deleteDev(order, j, device){
setCfg("known_devices_update", "d," + devicesList_Iface[order].getMac(j) + ";");
}
```

#### sendForm
provides the rest of the POST body we need to build

```
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


### /cgi/cgi_myNetwork.js
globals.js also calls the CGI's listed in /my_network.htm with the current timestamp as a parameter

eg:
```
/cgi/cgi_myNetwork.js?t=1592032536131
/cgi/cgi_owl.js?t=1592032536131
```
cgi_owl.js has some additional cfg vars to cgi_myNetwork.js but we only need 'known_devices_update'


cgi_myNetwork.js:
```
var known_device_list=[{...}] ( the known mac addresses ) 
addCfg("known_devices_update",94717334,'');  ( the current value of 'known_devices_update' cfg variable ) 
```


### /apply.cgi
finally the request is POST'd to apply.cgi - values broken down below

```
CMD=&GO=my_network.htm&SET0=53813335%3Dd%252C7C%253AFF%253A48%253A70%253A8D%253A8A%253B&pi=IANp88wHLhou6PA3

CMD=&GO=my_network.htm&SET0=  ( sendForm / deleteDev ) 
53813335  ( known_devices_update value from cgi_myNetwork ) 
%3D  ( sendForm ) 
d%252C  ( 'd%252C' = 'd%2C' = "d," from deleteDev ) 
7C %253A FF %253A 48 %253A 70 %253A 8D %253A 8A ( mac address where '%253A' = '%3A' = : )
%253B  ( '%253B' = '%3B' = ; end of command ) 
&pi=IANp88wHLhou6PA3 ( pi ) 
```
