#!/usr/bin/env python3

import re

print((re.match('1.3.6.1.2.1.1.1.0:.*',(open('smarthub.db').read())).group()).split(':')[1])
