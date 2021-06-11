# misc smarthub info that may save you some time

I spent a few hours diagnosing why some bridge interfaces on my homelab virtualisation setup were showing dropped RX packets. I initally suspected some powerline adapters; but it turned out to be the smarthub doing this kind of thing..

```
12:38:45.723880 64:cc:22:00:b9:fd (oui Unknown) > 01:80:c2:ef:03:fe (oui Unknown), ethertype Unknown (0xfe68), length 102:
	0x0000:  0303 0485 36ec 00c0 0180 c2ef 03fe 64cc  ....6.........d.
	0x0010:  2200 b9fd 0d36 4458 0303 0d85 36ec 00c0  "....6DX....6...
	0x0020:  8c51 218a 0b98 d6a0 e2dd 7347 8c51 2950  .Q!.......sG.Q)P
	0x0030:  57f1 d830 c222 7e41 d209 e1ab 1af5 7aae  W..0."~A......z.
	0x0040:  7761 7459 3c20 e7c3 7b9c c94c 5a51 276c  watY<...{..LZQ'l
	0x0050:  62a9 42e8 41e6 ef72                      b.B.A..r
```

I guess its something to do with whole home wifi discs. I ended up using nftables to drop them eg: 

```
#!/usr/sbin/nft -f

flush ruleset

table netdev filter {
    chain ingress {
    type filter hook ingress device enp0s25 priority 0; policy accept;
        meta protocol 0xfe68  drop
    }
}
```
