#!/usr/bin/env python3

import re

file=(open('smarthub.db').read())
print(file)

print((re.search('1.3.6.1.2.1.1.1.0_.*',(open('smarthub.db').read())).group()).split('_')[1])
print((re.search('1.3.6.1.2.1.1.3.0_.*',(open('smarthub.db').read())).group()).split('_')[1])
print((re.search('1.3.6.1.2.1.2.2.1.9.1_.*',(open('smarthub.db').read())).group()).split('_')[1])
print(re.search('1.3.6.1.2.1.1.1.0',(open('smarthub.db').read())))
print(re.search('1.3.6.1.2.1.1.3.0',(open('smarthub.db').read())))
